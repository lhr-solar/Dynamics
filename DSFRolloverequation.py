import math

def DSF(u,ms,h,rho,k,g,L,H,a,kr,b,kf,cf,cr,Tw,m):
    part_1 = Tw / (2 * H)
    part_2 = ((u ** 2) * ms * (h **2) * rho)
    part_3 = L * H * (k - ms * h * g)
    part_4 = (m * (u **2)) / (L ** 2)
    part_5 = (a / (2 * kr)) - (b / ( 2 * kf)) * math.cos(rho)
    part_6 = ((u ** 2) * ms * h * (cf - cr)) / (L * (k - ms * h * g))
    return(part_1 - (part_2 / (part_3 * (1- part_4 * part_5 - part_6))))
a = DSF(1,2,3,0.5,1,2,3,1,2,3,1,2,3,1,2,3)
print(a)
