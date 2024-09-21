%Simulates the car's dynamic behavior during the figure 8 test
function steeringSim(B,L,Rmax,b,m,path)
    %Establish physical parameters
    global currentPoint;
    W = m*9.81;
    a = L-b;
    Iz = 0.650*m*a*b;%0.650 is yaw dynamic index
    C = 170*180/pi;
    steerRatio = 5;
    Vx = 6;
    
    Wf = b*W/L;
    Wr = a*W/L;
    
    deltaMax = ackermann(B,L,Rmax,b);
    deltaMax = deltaMax(4);
    
    %Set initial values for physics simulation
    Vy0 = 0;
    omega0 = 0;
    X0 = 0;
    Y0 = 0;
    phi0 = pi/2;
    deltaSteer0 = deltaMax;
    x0 = [Vy0;omega0;X0;Y0;phi0;deltaSteer0];
    currentPoint = 1;

    %Run ode45 to solve for position and velocity
    fun = @(t,x) steeringSimEqn(t,x,B,L,Rmax,b,m,path,Iz,C,steerRatio,Vx);
    [t,x] = ode45(fun,0:0.1:18,x0);
    
    Vy = x(:,1);
    omega = x(:,2);
    X = x(:,3);
    Y = x(:,4);
    phi = x(:,5);
    deltaSteer = x(:,6);
    
    slipF = zeros(length(t), 1);
    slipR = zeros(length(t), 1);
    corneringF = zeros(length(t), 1);
    corneringR = zeros(length(t), 1);
    for n = 1:length(t)
        [xdot, y] = steeringSimEqn(t(n),x(n,:),B,L,Rmax,b,m,path,Iz,C,steerRatio,Vx);
        slipF(n) = y(1);
        slipR(n) = y(2);
        corneringF(n) = y(3);
        corneringR(n) = y(4);
    end
    
    %Graph the car's position, steering angle, slip angle, and cornering
    %forces
    subplot(2,2,1)
    scatter(path(:,1),path(:,2))
    hold on;
    plot(X,Y);
    title("Position");
    xlim([-30,30]);
    ylim([-30,30]);
    hold off;
    
    subplot(2,2,2)
    plot(t,deltaSteer);
    title("Steering Angle");
    
    subplot(2,2,3)
    plot(t,slipF);
    hold on;
    plot(t, slipR);
    title("Slip Angle");
    legend("Front Wheel","Rear Wheel");
    hold off;
    
    subplot(2,2,4)
    plot(t,corneringF)
    hold on;
    plot(t,corneringR);
    title("Cornering Force");
    legend("Front Wheel","Rear Wheel");
    hold off;
end