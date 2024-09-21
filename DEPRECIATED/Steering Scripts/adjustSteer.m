%Determine the direction the car needs to steer.
%Assumes the driver will be turning the wheel at a rate of 2 rotations per
%second.
function turnRate = adjustSteer(deltaSteer,deltaTarget,L,steerRatio,deltaMax)
    turnRate = 0;
    
    if(deltaSteer == 0)
        if(deltaTarget < 0)
            turnRate = -2/steerRatio;
        elseif(deltaTarget > 0)
            turnRate = 2/steerRatio;
        end
    else
        R = L/deltaSteer;
        pos = R*[sign(deltaSteer)*cos(deltaSteer), abs(sin(deltaSteer))];
        relativeTarget = pos+[-sin(deltaTarget), cos(deltaTarget)];
        if((relativeTarget(1)^2 + relativeTarget(2)^2) < R^2 && deltaSteer <= deltaMax)
            turnRate = 2/steerRatio;
        elseif((relativeTarget(1)^2 + relativeTarget(2)^2) > R^2 && deltaSteer >= -deltaMax)
            turnRate = -2/steerRatio;
        end
    end
    
end