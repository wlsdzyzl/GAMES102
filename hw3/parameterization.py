# parameterization methods
import numpy as np

pi = np.pi
half_pi = np.pi / 2
# compute the angle between two vector
def compute_angle(v1, v2):
    return np.arccos(np.inner(v1, v2) / (np.linalg.norm(v1).item() * np.linalg.norm(v2).item()))

# uniform parameterization
def uniform(points):
    step = 1.0 / (len(points)-1)
    return [x * step for x in range(len(points)) ]
# chordal parameterization
def chordal(points):
    dists = []
    sum_dists = 0
    for id in range(1, len(points)):
        dists.append( np.linalg.norm(points[id] - points[id - 1]).item() )
        sum_dists += dists[-1]
    t = [0]
    for d in dists:
        t.append(t[-1] + d / sum_dists)
    return t
# centripetal parameterization
def centripetal(points):
    dists = []
    sum_dists = 0
    for id in range(1, len(points)):
        dists.append( np.sqrt(np.linalg.norm(points[id] - points[id - 1]).item()) )
        sum_dists += dists[-1]
    t = [0]
    for d in dists:
        t.append(t[-1] + d / sum_dists)
    return t
# foley parameterization
def foley(points):
    dists = []
    angles = []
    foley_dists = []
    sum_dists = 0
    
    # get angles and dists
    for id in range(1, len(points) - 1):
        v1 = points[id - 1] - points[id]
        v2 = points[id + 1] - points[id]
        angle = compute_angle(v1, v2)
        angles.append( (pi - angle) if (angle > half_pi) else half_pi)
        if id == 1:
            dists.append(np.linalg.norm(v1).item())
        dists.append(np.linalg.norm(v2).item())

    
    foley_dists.append(dists[0] *( 1 +  1.5 * angles[1] * dists[0] /(dists[0] + dists[1]) ))
    for i in range(1, len(points) - 2):
        id = i - 1
        d = dists[id] *( 1 +  1.5 * angles[id] * dists[id - 1] /( dists[id - 1] + dists[id]) + 1.5 * angles[id+1] * dists[id] /(dists[id] + dists[id + 1]))
        foley_dists.append(d)
        sum_dists += d
    foley_dists.append(dists[len(points) - 2] *( 1 +  1.5 * angles[id] * dists[id - 1] /( dists[id - 1] + dists[id]) ))
    sum_dists += foley_dists[0]
    sum_dists += foley_dists[-1]
    t = [0]
    for d in foley_dists:
        t.append(t[-1] + d / sum_dists)
    #print(t)
    return t