function F = funRPInnerWheel(x,y,B,j,di,beta,d,q)
    F = ((B-j)/2 + q - x*sin(di + beta))^2 + (d - x*cos(di + beta))^2 - y^2;
end