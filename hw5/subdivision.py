# subdivision for approximating and interpolation
import numpy as np
def approximate_chaikin(points, n = 1000, closure = True):
    if len(points) >= n:
        return points
    points = np.array(points)
    new_points = []
    final_points = []
    if closure:
        # split
        for i in range(len(points)):
            next_id = (i+1) % len(points)
            new_points.append((points[i] + points[next_id]) / 2)
        # average
        for i in range(len(points)):
            next_id = (i+1) % len(points)
            final_points.append((points[i] + new_points[i]) / 2)
            final_points.append((points[next_id] + new_points[i]) / 2)
    else:
        # split
        for i in range(len(points) - 1):
            next_id = (i+1) % len(points)
            new_points.append((points[i] + points[next_id]) / 2)
        # average
        for i in range(len(points) - 1):
            next_id = (i+1) % len(points)
            final_points.append((points[i] + new_points[i]) / 2)
            final_points.append((points[next_id] + new_points[i]) / 2)
    return approximate_chaikin(final_points, n, closure)

def approximate_cubic(points, n = 1000, closure = True):
    if len(points) >= n:
        return points
    points = np.array(points)
    new_points = []
    final_points = []
    if closure:
        # split
        for i in range(len(points)):
            next_id = (i+1) % len(points)
            new_points.append((points[i] + points[next_id]) / 2)
        # average
        for i in range(len(points)):
            next_id = (i+1) % len(points)
            last_id = i-1
            final_points.append( points[i] * 0.75 +  points[next_id] * 0.125 +\
            points[last_id] * 0.125 )
            final_points.append( new_points[i])
    else:
        # split
        for i in range(len(points) - 1):
            next_id = (i+1) % len(points)
            new_points.append((points[i] + points[next_id]) / 2)
        # average
        for i in range(len(points)):
            next_id = (i+1) % len(points)
            last_id = i-1
            final_points.append( points[i] * 0.75 +  points[next_id] * 0.125 +\
            points[last_id]*0.125 )
            if i < len(new_points):
                final_points.append( new_points[i])
    return approximate_cubic(final_points, n, closure)
def interpolate(points, n = 1000, alpha = 0.2, closure = True):
    if len(points) >= n:
        return points
    if len(points) < 4:
        return points
    points = np.array(points)
    new_points = []
    if closure:
        for i in range(len(points)):
            last_id = i - 1
            next_id_0 = (i + 1) % len(points)
            next_id_1 = (i + 2) % len(points)
            new_p = (points[i] + points[next_id_0])/2 + alpha * \
                ((points[i] + points[next_id_0]) / 2 - (points[next_id_1] + points[last_id]) / 2)
            new_points.append(new_p)
        final_points = []
        for i in range(len(points)):
            final_points.append(points[i])
            final_points.append(new_points[i])
    else:
        for i in range(len(points)-1):
            last_id = i - 1
            if last_id < 0:
                last_id = 0
            next_id_0 = i + 1
            next_id_1 = i + 2
            if next_id_1 >= len(points):
                next_id_1 = len(points) - 1
            new_p = (points[i] + points[next_id_0])/2 + alpha * \
                ((points[i] + points[next_id_0]) / 2 - (points[next_id_1] + points[last_id]) / 2)
            new_points.append(new_p)
        final_points = []
        for i in range(len(points)-1):
            final_points.append(points[i])
            final_points.append(new_points[i])   
        final_points.append(points[-1])     
    return interpolate(final_points, n, alpha, closure)