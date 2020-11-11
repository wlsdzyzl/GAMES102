# an implementation of thomas algorithm, 
# which is used to solve tridiagonal matrix equation.
import numpy as np
# this function can be accelerated a lot.
# we don't need to save P, and Q matrix, cause we only need p,q

def solve(A, f):
    # crout decomposition
    n = A.shape[0]
    P = np.eye(n)
    Q = np.eye(n)
    last_q = 0
    for i in range(n):
        if i == 0:
            p = A[i][i]
        else:
            p = A[i][i] - A[i][i-1] * last_q
            P[i][i-1] = A[i][i-1]
        P[i][i] = p

        if i != n-1:
            q = A[i][i+1] / p
            last_q = q
            Q[i][i+1] = q
    # solve Py=f
    y = []
    last_y = 0
    
    for i in range(n):
        if i == 0:
            tmp_y = f[0] / P[0][0]
        else:
            tmp_y = (f[i] - A[i][i-1] * last_y) / P[i][i]
        y.append(tmp_y)
        last_y = tmp_y

    # solve Qx = y
    x = []
    last_x = 0
    for i in range(n):
        real_id = n-1 - i
        if i == 0:
            tmp_x = y[real_id]
        else:
            tmp_x = y[real_id]-Q[real_id][real_id+1]*last_x
        x.append(tmp_x)
        last_x = tmp_x
    x.reverse() 
    return np.array(x)

def solve_debug(A, b):
    # use svd to solve linear equation
    
    if A.shape[0] >= A.shape[1]:
        # overdetermined equation
        u, s, vt = np.linalg.svd(A)
        x = np.matmul (vt.T, np.matmul(u.T, b)[:s.shape[0]] / s)
    else:
        # underdetermined equation
        # overfit
        start = A.shape[1] - A.shape[0]
        A = A[:, start:]
        u, s, vt = np.linalg.svd(A)
        x = np.matmul (vt.T, np.matmul(u.T, b)[:s.shape[0]] / s)
        
        x = np.concatenate((np.zeros(start), x),axis = 0)
        
    return x