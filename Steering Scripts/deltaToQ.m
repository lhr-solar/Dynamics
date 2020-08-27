%Calculate the horizontal displacement of the rack for the desired turning
%angle
%-Inputs:
%delta = Desired turning angle of the car
%B = Distance between kingpin centerlines
%L = Wheelbase
%p = Length of the rack casing
%j = Length between rack's ball joints
%d = Distance between front axle and rack
%R = Desired turn radius
%b = Longitudinal position of CoM
%
%-Outputs:
%q = Horizontal displacement of the rack
function q = deltaToQ(delta,B,L,p,j,Rmax,b)
    R = b/sin(delta);
    Rri = R*cos(delta) - 0.5*B;
    dfi = atan(L/Rri);
    
    dim = rackAndPinion(B,L,p,j,Rmax,b);
    x = dim(1);
    y = dim(2);
    d = dim(3);
    beta = atan(B/(2*L));
    fun = @(q) funRPInnerWheel(x,y,B,j,dfi,beta,d,q);
    q0 = 0;
    q = fsolve(fun, q0);
end