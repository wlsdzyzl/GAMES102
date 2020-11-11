import numpy as np

# use bezier curve to interpolate

def deCasteljau_recur(points, t):
    if len(points) == 1:
        return points[0]
    new_points = []
    for i in range(len(points) - 1):
        new_points.append((1 - t) * points[i] + t * points[i+1]) 
    return deCasteljau_recur(new_points, t)
class bezier:
    def set_control_points(self, points):
        self.points = np.array(points)

    def deCasteljau(self, input_t):
        if input_t > 1 or input_t < 0:
            print("t should be in [0, 1]")
            return -1
        return deCasteljau_recur(self.points, input_t)
class bezier_interpolator:
    def set_points(self, points):
        self.points = np.array(points)
        self.beziers = [ bezier() for i in range(len(points) - 1)]
        # construct bezier points
        bezier_control_point_list = [[self.points[i]] for i in range(len(self.beziers))]
        
        for i in range(len(self.points) - 2):
            dist = (self.points[i+2] - self.points[i]) / 6
            bezier_control_point_list[i].append(self.points[i+1] - dist)
            bezier_control_point_list[i+1].append(self.points[i+1] + dist)
        for i in range(1, len(self.points)):
            bezier_control_point_list[i-1].append(self.points[i])
        # set bezier constrol points
        for i in range(len(self.beziers)):
            self.beziers[i].set_control_points(bezier_control_point_list[i])
    def set_parameter(self, t):
        self.t = t
    def deCasteljau(self, input_t):
        if input_t < 0 or input_t > 1:
            return -1
        group_id = -1
        for i in range(1, len(self.t)):
            if input_t <= self.t[i]:
                group_id = i - 1
                break
        if group_id == -1:
            group_id = len(self.t) - 2
        real_input_t = (input_t - self.t[group_id]) / \
            (self.t[group_id + 1] - self.t[group_id])
        if real_input_t > 1:
            real_input_t = 1
        if real_input_t < 0:
            real_input_t = 0
        # print(group_id, input_t, real_input_t)
        return self.beziers[group_id].deCasteljau(real_input_t)