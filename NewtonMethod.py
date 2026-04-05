## importing the modules
import numpy as np
## Function to compute difference table
def Table(x,y):
    n=len(x)
    x=np.asarray(x,dtype=float)
    y=np.asarray(y,dtype=float)
    diff_table=np.zeros((n,n),dtype=float)
    diff_table[0,:]=y
    for i in range(1,n):
        for k in range(0,n-i):
            diff_table[i,k]=diff_table[i-1,k+1]-diff_table[i-1,k]
    
    return diff_table

def NewtonPoly(diff_table,target,x,mode="forward"):
    n=len(x)
    product=1
    h=x[1]-x[0]
    if mode=="forward":
        result=diff_table[0,0]
        p=(target-x[0])/h ## p= (xp - x0)/(h) : where h is the common difference
        for i in range(1,n): ## Loop till the last row of the difference table
            product*=(p-(i-1))/i
            result+=(product*diff_table[i][0]) ## Add the current term to the previous term 
            ## because yk = y0 + del(y0)*p/1! + del2(y0)*p*(p-1)/2!...
    else:
        result=diff_table[0,n-1]
        p=(target-x[n-1])/h ## since p = (xp-xn)/(h) : where h is the common difference
        for i in range(1,n):
            product*=(p+(i-1))/i
            result+=product*diff_table[i][n-i-1]
            ## because yk= yn + del(yn)*p/1! + del2(yn)*p*(p+1)/2!...
    return result


## For calculating using arrays
def NewtonPolyMultiple(diff_table, targets, x, mode="forward"):
    return np.array([NewtonPoly(diff_table, t, x, mode) for t in targets])

if __name__ == "__main__":
    print("Run the code by importing into other file")