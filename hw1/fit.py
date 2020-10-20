import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


fig = plt.figure()
plt.plot([], [])
points = []
sigma = 1
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

def onclick(event):
    ix, iy = event.xdata, event.ydata
    points.append([ix, iy])

    plt.scatter(ix, iy, color="r")
    plt.draw()
    # global coords
    # coords.append((ix, iy))

    # if len(coords) == 2:
    #     fig.canvas.mpl_disconnect(cid)
    # return coords

if __name__ == "__main__":
    # generate points
    # points = np.array([[0.50, 0.40], 
    # [0.80, 0.30],
    # [0.30, 0.80],
    # [-0.40, 0.30],
    # [-0.30, 0.70]])
    # points = points * 10
    
    # interactive
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.xlim((-5, 5))
    plt.ylim((-2, 2))
    plt.show()
    


    plt.xlim((-5, 5))
    plt.ylim((-2, 2))
    # draw original points
    points = np.array(points)
    #print(points)
    x = points[:,0]
    y = points[:,1]
    plt.scatter(x, y, color='red')
    
    x_axis = np.linspace(-5, 5, 100)
    
    # draw polynomial fitting
    w_1 = polynomial_fitting(points)
    
    x_matrix = np.zeros((x_axis.shape[0], w_1.shape[0]))
    x_power = np.ones_like(x_axis)
    
    for i in range(w_1.shape[0]):
        x_matrix[:,i] += x_power
        x_power = np.multiply(x_power, x_axis)
    y1 = np.matmul(x_matrix, w_1)
    plt.plot(x_axis, y1, label = "polynomial interpolation")

    # draw gaussian fitting
    w_2 = gaussian_fitting(points)

    x_matrix = np.zeros((x_axis.shape[0], w_2.shape[0]))
    x_matrix[:,0] = np.ones_like(x_axis)
    for i in range(0, w_2.shape[0]-1):
        tmp_x = x_axis - np.ones_like(x_axis) * x[i]
        x_matrix[:, i + 1] = np.exp( - np.power(tmp_x, 2) / (2 * sigma * sigma))
        
    y2 = np.matmul(x_matrix, w_2)
    plt.plot(x_axis, y2, label = "gaussian interpolation")

    # draw regression fitting
    # number of parameters
    n = 5

    w_3 = regression(points, n)
    
    x_matrix = np.zeros((x_axis.shape[0], w_3.shape[0]))
    x_power = np.ones_like(x_axis)
    
    for i in range(w_3.shape[0]):
        x_matrix[:,i] += x_power
        x_power = np.multiply(x_power, x_axis)
    y3 = np.matmul(x_matrix, w_3)
    plt.plot(x_axis, y3, label = "regression")

    # draw ridge regression

    w_4 = ridge_regression(points, n)
    
    x_matrix = np.zeros((x_axis.shape[0], w_4.shape[0]))
    x_power = np.ones_like(x_axis)
    
    for i in range(w_4.shape[0]):
        x_matrix[:,i] += x_power
        x_power = np.multiply(x_power, x_axis)
    y4 = np.matmul(x_matrix, w_4)
    plt.plot(x_axis, y4, label = "ridge regression")

    print(np.linalg.norm(w_3), np.linalg.norm(w_4))
    plt.legend()
    plt.show()
