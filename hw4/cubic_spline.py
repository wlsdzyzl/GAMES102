# construct equation for cubic spline
import numpy as np
import thomas as tms
class cubic_spline:
    def set_points(self, points):
        self.points = points
    def construct_cubic_spline(self, boundary = 0):
        # if boundary condition is zero, we fix the 
        # second derivative of points at both ends.
        # else, we fix the first derivative. 
        h = [self.points[i][0] - self.points[i-1][0] for i in range(1,len(self.points))]
        A = np.zeros((len(self.points), len(self.points)))
        if boundary == 0:
            for i in range(len(self.points)):
                if i == len(self.points) - 1 or i == 0:
                    A[i][i] = 1
                else:
                    A[i][i-1] = h[i-1]
                    A[i][i+1] = h[i]
                    A[i][i] = 2 * (h[i] + h[i-1])
                
        else:
            for i in range(len(self.points)):    
                if i == 0:
                    A[i][i] = 2 * h[i]
                    A[i][i+1] = h[i]
                elif i == len(self.points) - 1:
                    A[i][i] = 2 * h[i-1]
                    A[i][i-1] = h[i-1]
                else:
                    A[i][i-1] = h[i-1]
                    A[i][i+1] = h[i]
                    A[i][i] = 2 * ( h[i] + h[i-1])
        f = []
        f.append(0)
        second_tmp = 0
        for i in range(1, len(self.points)-1):
            if i == 1:
                second_tmp = (self.points[1][1] - self.points[0][1]) / h[0]
            first_tmp = (self.points[i+1][1] - self.points[i][1])/h[i]
            f.append(6 * (first_tmp - second_tmp))
            second_tmp = first_tmp
        f.append(0)
        
        # solve equation
        x = tms.solve(A, f)
        # compute a
        # print(A, f)
        # print("x:", x)
        self.a = [self.points[i][1] for i in range(len(h))]
        
        # compute b
        self.b = []
        for i in range(len(h)):
            self.b.append( (self.points[i+1][1] - self.points[i][1])/h[i] - x[i]*h[i] / 2 \
                - (x[i+1] - x[i])* h[i] / 6 )
        # compute c
        self.c = [x[i]/2 for i in range(len(h))]

        # compute d
        self.d = [(x[i+1] - x[i])/(6 * h[i])  for i in range(len(h))]
        print(self.a)
        print(self.b)
        print(self.c)
        print(self.d)
    def new_points(self, input_x):
        # determine the range of x
        group_id = -1
        if input_x <= self.points[0][0]:
            group_id = 0
        for i in range(1, len(self.points)):
            if input_x <= self.points[i][0]:
                group_id = i-1
                break
        if group_id == -1:
            group_id = len(self.points)-2
        # compute the value

        tmp_x = input_x - self.points[group_id][0] 
        output_y = self.a[group_id] + self.b[group_id] * tmp_x \
            + self.c[group_id] * tmp_x * tmp_x \
            + self.d[group_id] * tmp_x * tmp_x * tmp_x

        return output_y
    # construct g1_0
    def construct_cubic_spline_g1_0(self, times):
        h = [self.points[i][0] - self.points[i-1][0] for i in range(1,len(self.points))]
        A = np.zeros((len(self.points), len(self.points)))

        for i in range(len(self.points)):
            if i == len(self.points) - 1 or i == 0:
                A[i][i] = 1
            else:
                A[i][i-1] = h[i-1]
                A[i][i+1] = times * h[i]
                A[i][i] = 2 * (  h[i] +times * h[i-1])
        f = []
        f.append(0)
        second_tmp = 0
        for i in range(1, len(self.points)-1):
            if i == 1:
                second_tmp = (self.points[1][1] - self.points[0][1]) / h[0]
            first_tmp = (self.points[i+1][1] - self.points[i][1])/h[i]
            f.append(6 * (first_tmp - second_tmp))
            second_tmp = first_tmp
        f.append(0)
        
        # solve equation
        x = tms.solve(A, f)
        # compute a
        # print(A, f)
        # print("x:", x)
        self.a = [self.points[i][1] for i in range(len(h))]
        
        # compute b
        self.b = []
        for i in range(len(h)):
            self.b.append( (self.points[i+1][1] - self.points[i][1])/h[i] - x[i]*h[i] / 2 \
                - (times * x[i+1] - x[i])* h[i] / 6 )
        # compute c
        self.c = [x[i]/2 for i in range(len(h))]

        # compute d
        self.d = [( times * x[i+1] - x[i])/(6 * h[i])  for i in range(len(h))]
        # for i in range(1,len(self.points) - 1):
        #     tmp_x_l = self.points[i][0] - self.points[i-1][0]
        #     output_y_l = self.b[i-1]  \
        #         + 2 * self.c[i-1] * tmp_x_l \
        #         + 3 * self.d[i-1] * tmp_x_l * tmp_x_l
        #     tmp_x_r = 0
        #     output_y_r = self.b[i]  \
        #         + 2 * self.c[i] * tmp_x_r \
        #         + 3 * self.d[i] * tmp_x_r * tmp_x_r

        #     # output_y_l =  \
        #     #     + 2 * self.c[i-1] \
        #     #     + 6 * self.d[i-1] * tmp_x_l 
        #     # tmp_x_r = 0
        #     # output_y_r = \
        #     #     + 2 * self.c[i] * 2
        #     print(output_y_l, output_y_r)
    def construct_cubic_spline_g1_1(self, times):
        # if boundary condition is zero, we fix the 
        # second derivative of points at both ends.
        # else, we fix the first derivative. 
        h = [self.points[i][0] - self.points[i-1][0] for i in range(1,len(self.points))]
        A = np.zeros((len(self.points), len(self.points)))

        for i in range(len(self.points)):
            if i == len(self.points) - 1 or i == 0:
                A[i][i] = 1
            else:
                A[i][i-1] = h[i-1]
                A[i][i+1] = times * h[i]
                A[i][i] = 2 * ( times * h[i] + h[i-1])
        f = []
        f.append(0)
        second_tmp = 0
        for i in range(1, len(self.points)-1):
            if i == 1:
                second_tmp = (self.points[1][1] - self.points[0][1]) / h[0]
            first_tmp = (self.points[i+1][1] - self.points[i][1])/h[i]
            f.append(6 * (times * first_tmp - second_tmp))
            second_tmp = first_tmp
        f.append(0)
        
        # solve equation
        x = tms.solve(A, f)
        # compute a
        # print(A, f)
        # print("x:", x)
        self.a = [self.points[i][1] for i in range(len(h))]
        
        # compute b
        self.b = []
        for i in range(len(h)):
            self.b.append( (self.points[i+1][1] - self.points[i][1])/h[i] - x[i]*h[i] / 2 \
                - (x[i+1] - x[i])* h[i] / 6 )
        # compute c
        self.c = [x[i]/2 for i in range(len(h))]

        # compute d
        self.d = [(x[i+1] - x[i])/(6 * h[i])  for i in range(len(h))]
        
P = [[0, -0.03], [0.24378, -0.15], [0.402016, -0.33], [0.705144, -0.5], [1, -0.44]]
cs = cubic_spline()
cs.set_points(P)
cs.construct_cubic_spline()