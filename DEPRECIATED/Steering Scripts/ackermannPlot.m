function ackermannPlot(B,L,R,b)
    %Determine radii of rear wheels' paths
    Dcom = asin(b/R);
    Rri = R*cos(Dcom) - 0.5*B;
    Rro = Rri + B;
    
    %Determine angles of front wheels
    Dfi = atan(L/Rri);
    Dfo = atan(L/Rro);
    
    %Determine radii of front wheels' paths
    Rfi = Rri/cos(Dfi);
    Rfo = Rro/cos(Dfo);
    
    %Find coordinates for paths of wheels and CoM
    X = zeros(5,360);
    Y = zeros(5,360);
    for n = 1:360
        d = 2*pi*(n/360);
        X(1:end, n) = cos(d)*[R;Rri;Rro;Rfi;Rfo];
        Y(1:end, n) = sin(d)*[R;Rri;Rro;Rfi;Rfo];
    end
    
    %Create plot points for drawing car schematic
    RearAxle = [-Rro, 0; -Rri, 0];
    FrontAxle = [-Rro, L; -Rri, L];
    Centerline = [(-Rro + 0.5*B), 0; (-Rro + 0.5*B), L];
    RearInner = [-Rri, -0.5; -Rri, 0.5];
    RearOuter = [-Rro, -0.5; -Rro, 0.5];
    FrontInner = [(-Rri - 0.5*sin(Dfi)), (L - 0.5*cos(Dfi)); (-Rri + 0.5*sin(Dfi)), (L + 0.5*cos(Dfi))];
    FrontOuter = [(-Rro - 0.5*sin(Dfo)), (L - 0.5*cos(Dfo)); (-Rro + 0.5*sin(Dfo)), (L + 0.5*cos(Dfo))];
    PointsX = [(-Rro + 0.5*B), -Rri, -Rro, -Rri, -Rro];
    PointsY = [b, 0, 0, L, L];
    
    %Plot paths and wheel orientations
    plot(X(1, 1:end), Y(1, 1:end),'r');
    hold on;
    plot(X(2, 1:end), Y(2, 1:end),'g');
    plot(X(3, 1:end), Y(3, 1:end),'b');
    plot(X(4, 1:end), Y(4, 1:end)),'m';
    plot(X(5, 1:end), Y(5, 1:end)),'c';
    
    plot(RearAxle(1:end, 1), RearAxle(1:end, 2), 'k');
    plot(FrontAxle(1:end, 1), FrontAxle(1:end, 2), 'k');
    plot(Centerline(1:end, 1), Centerline(1:end, 2), 'k');
    plot(RearInner(1:end, 1), RearInner(1:end, 2), 'k');
    plot(RearOuter(1:end, 1), RearOuter(1:end, 2), 'k');
    plot(FrontInner(1:end, 1), FrontInner(1:end, 2), 'k');
    plot(FrontOuter(1:end, 1), FrontOuter(1:end, 2), 'k');
    scatter(PointsX, PointsY, 'ok')
    hold off;
    
    disp("Inner Wheel Angle: " + rad2deg(Dfi));
    disp("Outer Wheel Angle: " + rad2deg(Dfo));
end