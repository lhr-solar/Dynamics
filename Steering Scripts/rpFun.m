%System of nonlinear equations for solving rack and pinion dimensions
function F = rpFun(dim,B,j,di,do,beta,q)
    F(1) = ((B-j)/2 - dim(1)*sin(beta))^2 + (dim(3) - dim(1)*cos(beta))^2 - dim(2)^2;
    F(2) = ((B-j)/2 - q + dim(1)*sin(do - beta))^2 + (dim(3) - dim(1)*cos(do - beta))^2 - dim(2)^2;
    F(3) = ((B-j)/2 + q - dim(1)*sin(di + beta))^2 + (dim(3) - dim(1)*cos(di + beta))^2 - dim(2)^2;
end