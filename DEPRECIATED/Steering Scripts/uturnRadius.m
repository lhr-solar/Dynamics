function uturnRadius(B,L,b)
    laneWidth = 16;
    maxRadius = 0.5*laneWidth - 0.5*B;
    maxAngles = ackermann(B,L,maxRadius,b);
    anglesSafety25 = ackermann(B,L,(maxRadius - 0.25),b);
    anglesSafety50 = ackermann(B,L,(maxRadius - 0.50),b);
    
    disp("Required Turn Radius: " + maxRadius + "; Inner Angle: " + maxAngles(1) + "; Outer Angle: " + maxAngles(2));
    disp("Saftey Turn Radius(-0.25 m): " + (maxRadius - 0.25) + "; Inner Angle: " + anglesSafety25(1) + "; Outer Angle: " + anglesSafety25(2));
    disp("Safety Turn Radius(-0.50 m): " + (maxRadius - 0.5) + "; Inner Angle: " + anglesSafety50(1) + "; Outer Angle: " + anglesSafety50(2));
end