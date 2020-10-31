# fit.py from hw1
import numpy as np
# 2d points
# interpolation----polynomial fitting

def solve(A, b):
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

def polynomial_fitting(points):
    # solve linear function
    n = len(points)
    x_array = points[:,0]
    y_array = points[:,1]

    A = np.zeros((n, n))
    x_power = np.ones_like(x_array)
    for i in range(n):
        A[:,i] = x_power
        x_power = np.multiply(x_power, x_array)
    #print(A)
    r = solve(A, y_array)
    return r
# interpolation----Gaussian fitting
def gaussian_fitting(points):
    n = len(points)
    x_array = points[:,0]
    y_array = points[:,1]
    A = np.zeros((n , n + 1))
    A[:,0] = np.ones_like(x_array)
    for i in range(n):
        tmp_x = x_array -  np.ones_like(x_array) * x[i]
        A[:, i+1] = np.exp( - np.power(tmp_x, 2) / (2 * sigma * sigma))
    # b0 = 0
    # A = np.row_stack((A, np.zeros(n+1)))
    # A[n][0] = 1
    # y_array = np.append(y_array, 0)
    r = solve(A, y_array)
    return r
# approximate fitting----least squares
# 3 unknown coefficients

def regression(points, n = 3):
    point_size = len(points)
    x_array = points[:,0]
    y_array = points[:,1]
    A = np.zeros((point_size, n))
    x_power = np.ones_like(x_array)
    for i in range(n):
        A[:,i] = x_power
        x_power = np.multiply(x_power, x_array)
    r = solve(A, y_array)
    
    return r
# approximate fitting----ridge regression
def ridge_regression(points, n = 3):
    point_size = len(points)
    x_array = points[:,0]
    y_array = points[:,1]
    A = np.zeros((point_size, n))
    x_power = np.ones_like(x_array)
    for i in range(n):
        A[:,i] = x_power
        x_power = np.multiply(x_power, x_array)
    A = np.concatenate((A, np.eye(n)), axis = 0)
    y_array = np.concatenate((y_array, np.zeros(n)))
    r = solve(A, y_array)
    
    return r