import taichi as ti
import parameterization as pr
import fitting as fit
import numpy as np
# use taichi to visualize the fitting results

points = []
# draw on canvas
canvas_points = []
lines = []
t_lines = []
res = (800, 600)

x_range = [-4, 4]
y_range = [-3, 3]
x_len = x_range[1] - x_range[0]
y_len = y_range[1] - y_range[0]
p_m = 0
f_m = 0

def get_coordinates(p):
    return [x_range[0] +  p[0] * x_len, y_range[0] + p[1] * y_len]

def get_canvas_coor(p):
    return [(p[0] - x_range[0]) / x_len, ( p[1] - y_range[0]) / y_len ]


def draw(gui):
    # draw points
    for p in canvas_points:
        gui.circle(p, 0xFF0000, 8)
    # draw lines
    for i in range(len(lines) - 1):
        gui.line(lines[i], lines[i+1])
    # draw t
    for p in t_lines:
        gui.circle(p, 0x00FF44, 4) 
    for i in range(len(t_lines) - 1):
        gui.line(t_lines[i], t_lines[i+1], color = 0x00FF44)
    
    

# use gui to generate points
gui = ti.GUI("From Points to Curve", res)
# add button 
KEY_CLEAR = gui.button('clear')
KEY_UNIFORM = gui.button('uniform')
KEY_CHORDAL = gui.button('chordal')
KEY_CENTRI = gui.button('centripetal')
KEY_FOLEY = gui.button('foley')
rotate_angle = gui.slider('rotate angle', 0, 180, step=180.0 / 100)
KEY_ROTATE = gui.button('rotate')
def get_rotation_matrix(theta):
    theta = np.radians(theta)
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, -s), (s, c)))

while gui.running:
    event = None
    
    if gui.get_event():
        event = gui.event
    if event:
        # add point
        #print(event.pos, event.key, event.type)
        if event.key == ti.GUI.RMB and event.type == ti.GUI.RELEASE:
            mouse_x, mouse_y = gui.get_cursor_pos()
            canvas_points.append([mouse_x, mouse_y])
            points.append(get_coordinates([mouse_x, mouse_y]))
            #print(points)            
        if event.key == KEY_CLEAR:
            points = []
            canvas_points = []
            lines = []
            t_lines = []
        # rotate the points
        if event.key == KEY_ROTATE:
            rotation_matrix = get_rotation_matrix(rotate_angle.value)
            for i in range(len(canvas_points)):
                trans_p = np.matmul(rotation_matrix, np.array([[points[i][0]], [points[i][1]] ]))
                points[i][0], points[i][1] =  trans_p[0][0], trans_p[1][0]
                canvas_points[i] = get_canvas_coor(points[i])
        if event.key == KEY_UNIFORM :
            p_m = 0
        if event.key == KEY_CHORDAL :
            p_m = 1
            
        if event.key == KEY_CENTRI :
            p_m = 2
            
        if event.key == KEY_FOLEY :
            p_m = 3
            t = pr.foley(np.array(points))
        if event.key == KEY_UNIFORM or event.key == KEY_CHORDAL or event.key == KEY_CENTRI or event.key == KEY_FOLEY or event.key == KEY_ROTATE:
            #t = [t_i * x_len + x_range[0] for t_i in t]
            #print(t)
            if p_m == 0:
                t = pr.uniform(np.array(points))
            if p_m == 1:
                t = pr.chordal(np.array(points))
            if p_m == 2:
                t = pr.centripetal(np.array(points))
            if p_m == 3:
                t = pr.foley(np.array(points))

            tx = []
            ty = []
            for i in range(len(t)):
                tx.append([t[i], points[i][0]])
                ty.append([t[i], points[i][1]])
            # use polynomial interpolation
            
            Wx = fit.polynomial_fitting(np.array(tx))
            Wy = fit.polynomial_fitting(np.array(ty))
            t_axis = np.linspace(0, 1, 100)
            t_power = np.ones_like(t_axis)
            t_matrix = np.zeros((t_axis.shape[0], Wx.shape[0]))
            
            
            for i in range(Wx.shape[0]):
                t_matrix[:,i] += t_power
                t_power = np.multiply(t_power, t_axis)
            x_axis = np.matmul(t_matrix, Wx)
            y_axis = np.matmul(t_matrix, Wy)

            # get_canvas_coor to transform points into canvas
            lines = []
            t_lines = []
            for i in range(len(t)):
                t_lines.append([t[i], 0.1])
            for i in range(len(t_axis)):
                lines.append(get_canvas_coor([x_axis[i], y_axis[i]]))
            
    draw(gui)
    if p_m == 0:
        gui.text("using uniform parameterization",(0.01, 0.99), 24)
    if p_m == 1:
        gui.text("using chordal parameterization",(0.01, 0.99), 24)
    if p_m == 2:
        gui.text("using centripetal parameterization",(0.01, 0.99), 24)
    if p_m == 3:
        gui.text("using foley parameterization",(0.01, 0.99), 24)   
    gui.show()    

            
            