import numpy as math

v=65#mph
a=.35*2#meters
b=.65*2#meters
m=2224/9.81#kg
k1=867#newtons per degree
k3=k1#newtons per degree


vt=(((a+b)*(a+b))*k1*k3*2)/(m*(a*k1-b*k3))#theoretical velocity
vt=math.sqrt(vt)

vt=vt*2.23694#meters per second to miles per hour

print(vt)
print("vt is stable")
#per model, if impossible to solve, we are stable at all speeds








