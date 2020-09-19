%Calculates position, velocity, orientation, and steering angle over time
function [xdot, y] = steeringSimEqn(t,x,B,L,Rmax,b,m,path,Iz,C,steerRatio,Vx)
    global currentPoint;
    Vy = x(1);
    omega = x(2);
    X = x(3);
    Y = x(4);
    phi = x(5);
    deltaSteer = x(6);
    
    %Determine if the car is close enough to the next target in the path.
    %If so, then it will move on to the next point.
    a = L-b;
    minDistance = 3.5*L;
    targetPoint = path(currentPoint,:);
    distance = sqrt((X-targetPoint(1))^2 + (Y-targetPoint(2))^2);
    while (distance < minDistance)
        if (currentPoint < length(path))
            currentPoint = currentPoint + 1;
        else
            currentPoint = 1;
        end
        
        targetPoint = path(currentPoint,:);
        distance = sqrt((X-targetPoint(1))^2 + (Y-targetPoint(2))^2);
    end
    
    %Calculate the direction pointing towards the next point
    ePhi = [cos(phi), sin(phi)];
    targetVector = [targetPoint(1) - (X+cos(phi)*a), targetPoint(2) - (Y+sin(phi)*a)];
    deltaTarget = atan2(ePhi(1)*targetVector(2)-ePhi(2)*targetVector(1), ePhi(1)*targetVector(1)+ePhi(2)*targetVector(2));
    
    %Calculate maximum steering angle
    deltaMax = ackermann(B,L,Rmax,b);
    deltaMax = deltaMax(4);
    
    %Calculate slip angle and cornering force
    alphaf = deltaSteer - atan((a*omega+Vy)/Vx);
    alphar = atan((b*omega-Vy)/Vx);
    Fyf = 2*C*alphaf;
    Fyr = 2*C*alphar;
    
    %Calculate rates of change
    Vy_dot = (-m*Vx*omega + Fyr + Fyf*cos(deltaSteer))/m;
    omega_dot = (a*Fyf*cos(deltaSteer) - b*Fyr)/Iz;
    X_dot = Vx*cos(phi) - Vy*sin(phi);
    Y_dot = Vx*sin(phi) + Vy*cos(phi);
    phi_dot = omega;
    if(sign(deltaSteer) ~= sign(deltaTarget))
        deltaSteer_dot = sign(deltaTarget)*0.5/steerRatio
    else
        deltaSteer_dot = adjustSteer(deltaSteer, deltaTarget, L, steerRatio, deltaMax);
    end
    
    xdot = [Vy_dot;omega_dot;X_dot;Y_dot;phi_dot;deltaSteer_dot];
    y = [alphaf,alphar,Fyf,Fyr];
end