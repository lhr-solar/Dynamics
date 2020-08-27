%Determines the angles of the front wheels while turning, based on Ackermann Steering Geometry
%-Inputs:
%B = Length of the axles
%L = Distance between axles
%R = Desired turn radius taken at Center of Mass(CoM)
%b = Longitudinal distance from rear axle to CoM
%
%-Outputs:
%angles = [Front Inner Wheel Angle, Front Outer Wheel Angle, CoM angle of Travel]
function angles = ackermann(B,L,R,b)
    %Determine radii of rear wheels' paths
    Dcom = acsc(R/b);
    Rri = R*cos(Dcom) - 0.5*B;
    Rro = Rri + B;
    
    %Determine angles of front wheels
    Dfi = rad2deg(atan(L/Rri));
    Dfo = rad2deg(atan(L/Rro));
    
    angles = [Dfi, Dfo, Dcom];
end