%Approximates the lateral force on each tire
%-Inputs
%L = Length between axles
%R = Desired turn radius taken at Center of Mass(CoM)
%b = Longitudinal distance from rear axle to CoM
%W = Weight
%v = Velocity
%
%-Outputs:
%cForces = [Total force on front wheels, Total force on rear wheels]
function cForces = cornering(L, R, b, W, v)
    g = 9.81;
    m = W/g;
    a = L - b;
    
    Fr = m*a*(v^2)/(L*R);
    Ff = Fr * (a/b);
    
    cForces = [Ff, Fr];
end