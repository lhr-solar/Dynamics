function delta = qToDelta(q,B,L,p,j,Rmax,b)
    dim = rackAndPinion(B,L,p,j,Rmax,b);
    x = dim(1);
    y = dim(2);
    d = dim(3);
    beta = atan(B/(2*L));

    fun = @(di) funRPInnerWheel(x,y,B,j,di,beta,d,q);
    di0 = 0;
    di = fsolve(fun, di0);
    
    Rri = L/tan(di);
    delta = atan(b/(Rri+0.5*B));
end