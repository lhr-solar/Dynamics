%Determines the tie-rod lengths necessary for the given car dimensions
%-Inputs
%B = Distance between kingpin centerlines
%L = Wheelbase
%p = Length of the rack casing
%j = Length between rack's ball joints
%d = Distance between front axle and rack
%Rmax = Max turn radius
%b = Longitudinal position of CoM
%
%-Outputs
%dimensions = [x,y,q]
%x = Steering arm length
%y = Tie-rod length(when viewed top-down)
%q = Displacement of rack

function dimensions = rackAndPinion(B,L,p,j,Rmax,b)
    %Determine front wheel rotations and car's Ackermann Angle
    wheels = ackermann(B,L,Rmax,b);
    di = deg2rad(wheels(1));
    do = deg2rad(wheels(2));
    beta = atan(B/(2*L));
    q = (j-p)/2; %Determine the displacement of the rack at maximum turn angle
    
    %Solve system of equations to determine dimensions
    fun = @(dim) rpFun(dim,B,j,di,do,beta,q);
    dim0 = [0, 0, 0];
    options = optimoptions('fsolve','Algorithm','trust-region');
    soln = fsolve(fun,dim0,options);
    
    dimensions = soln;
end