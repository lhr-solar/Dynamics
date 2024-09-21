function drawRackAndPinion(B,L,W,p,j,R,b)
    dim = rackAndPinion(B,L,p,j,R,b);
    x = abs(dim(1));
    y = abs(dim(2));
    d = abs(dim(3));
    beta = atan(B/(2*L));
    phi = atan((d-x*cos(beta))/(0.5*B-0.5*j-x*sin(beta)));
    
    drawLine([-0.5*W,0.5*L;0.5*W,0.5*L]);%Front Axle
    hold on;
    drawLine([-0.5*W,-0.5*L;0.5*W,-0.5*L]);%Rear Axle
    drawLine([0,-0.5*L;0,0.5*L]);%Centerline
    drawLine([-0.5*B,0.5*L;-0.5*B+x*sin(beta),0.5*L-x*cos(beta)]);%Left Steering Arm
    drawLine([0.5*B,0.5*L;0.5*B-x*sin(beta),0.5*L-x*cos(beta)]);%Right Steering Arm
    drawLine([-0.5*j,0.5*L-d;-0.5*j-y*cos(phi),0.5*L-d+y*sin(phi)]);%Left Tie-Rod
    drawLine([0.5*j,0.5*L-d;0.5*j+y*cos(phi),0.5*L-d+y*sin(phi)]);%Right Tie-Rod
    drawLine([-0.5*j,0.5*L-d;0.5*j,0.5*L-d]);%Rack Line
    drawLine([-0.5*p,0.5*L-d+0.01;0.5*p,0.5*L-d+0.01;0.5*p,0.5*L-d-0.01;-0.5*p,0.5*L-d-0.01;-0.5*p,0.5*L-d+0.01]);%Rack Casing
    drawLine([-0.5*W,0.5*L+0.2;-0.5*W,0.5*L-0.2]);%Front Left Wheel
    drawLine([-0.5*W,-0.5*L+0.2;-0.5*W,-0.5*L-0.2]);%Rear Left Wheel
    drawLine([0.5*W,0.5*L+0.2;0.5*W,0.5*L-0.2]);%Front Right Wheel
    drawLine([0.5*W,-0.5*L+0.2;0.5*W,-0.5*L-0.2]);%Rear Right Wheel
    hold off;
    
    xlim([-2,2]);
    ylim([-2,2]);
end