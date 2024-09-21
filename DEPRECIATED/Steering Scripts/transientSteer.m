function path = transientSteer(di,df,t,v,position,direction)
    rackshift = deltaToQ(df)*sign(df)-deltaToQ(di)*sign(di);
end