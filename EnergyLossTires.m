weightTire = 2224.11/4; %this if assuming the car has a weight of 500 lbf in which we converted to Newtons
radius = 0.3556; %this is assuming 14 inch tires in meters
b = .0045 * radius; %.0045
velocity = 20.1168; %this is assuming 45 mph in meter/s

Power = RollingPower(weightTire, b, radius, velocity);

fprintf("\nPower Loss due to Rolling Resistance is %f Watts\n", Power);


SolarEnergy = 800; %in watts
Airdrag = SolarEnergy - Power;

fprintf("\nPower Loss due to Airdrag is %f Watts\n", Airdrag);