import csv
import numpy as np

def draw_samples(n):
    a0,a1 = -0.3,0.5
    trueX =  np.random.uniform(-1,1,n)
    trueT = a0 + (a1*trueX)
    return trueX, trueT + np.random.normal(0,0.2,n)

N = 12
x,t = draw_samples(N)
print 'x = %s'%[round(_x,2) for _x in x]
print 't = %s'%[round(_t,2) for _t in t]

writer = csv.writer(open('linreg-data.csv','w'))
writer.writerow(["x","y"])

for i in range(N):
    writer.writerow([round(x[i],3),round(t[i],3)])
