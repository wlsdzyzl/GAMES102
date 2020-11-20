import taichi as ti
import numpy as np
from subdivision import approximate_chaikin as apx_ck
from subdivision import approximate_cubic as apx_cb
from subdivision import interpolate as itp
# use taichi to visualize the fitting results

points = []
EPS = 0.1
max_n = 1000
# draw on canvas
canvas_points = []
# chaikin 0
lines_1 = []
# chaikin 1
lines_2 = []
# cubic 0
lines_3 = []
# cubic 1
lines_4 = []
# interpolation 0
lines_5 = []
# interpolation 1
lines_6 = []
res = (800, 600)
x_range = [-4, 4]
y_range = [-3, 3]


x_len = x_range[1] - x_range[0]
y_len = y_range[1] - y_range[0]
color_tab = [0x1f77b4, 0xff7f0e, 0x2ca02c, 0xd62728, 0x9467bd, 0x8c564b, 0xe377c2, 0x7f7f7f, 0xbcbd22, 0x17becf]
chosen_point_id = -1
def get_coordinates(p):
    return [x_range[0] +  p[0] * x_len, y_range[0] + p[1] * y_len]

def get_canvas_coor(p):
    return [(p[0] - x_range[0]) / x_len, ( p[1] - y_range[0]) / y_len ]

# use gui to generate points
gui = ti.GUI("Subdivision", res)
# add slide
selector = gui.slider('selector', 1, 7.99, step=1)
alpha_selector = gui.slider('alpha', 0.01, 1, step=0.01)
# add button 
KEY_CLEAR = gui.button('clear')


def draw():
    # draw points
    for p in canvas_points:
        gui.circle(p, 0xFF0000, 8)
    # draw lines
    r = 1.5
    selector_value = int(selector.value)
    if selector_value == 1 or selector_value == 7:
        for i in range(len(lines_1) - 1):
            gui.line(lines_1[i], lines_1[i+1], color=color_tab[0], radius= r)
    if selector_value == 2 or selector_value == 7:
        for i in range(len(lines_2) - 1):
            gui.line(lines_2[i], lines_2[i+1], color=color_tab[1], radius = r) 
    if selector_value == 3 or selector_value == 7:
        for i in range(len(lines_3) - 1):
            gui.line(lines_3[i], lines_3[i+1], color=color_tab[2], radius = r)    
    if selector_value == 4 or selector_value == 7:
        for i in range(len(lines_4) - 1):
            gui.line(lines_4[i], lines_4[i+1], color=color_tab[3], radius = r) 
    if selector_value == 5 or selector_value == 7:
        for i in range(len(lines_5) - 1):
            gui.line(lines_5[i], lines_5[i+1], color=color_tab[4], radius = r) 
    if selector_value == 6 or selector_value == 7:
        for i in range(len(lines_6) - 1):
            gui.line(lines_6[i], lines_6[i+1], color=color_tab[5], radius = r) 

def compute_and_draw():
    global points
    global lines_1
    global lines_2
    global lines_3
    global lines_4
    global lines_5
    global lines_6
    if len(points)>= 4:

        # use polynomial interpolation
        canvas_points = []
        alpha = alpha_selector.value
        # get_canvas_coor to transform points into canvas
        generate_points = apx_ck(points, max_n, False)
        lines_1 = []
        for i in range(len(generate_points)):
            lines_1.append(get_canvas_coor(generate_points[i]))
        
        generate_points = apx_ck(points, max_n, True)
        lines_2 = []
        for i in range(len(generate_points)):
            lines_2.append(get_canvas_coor(generate_points[i]))

        generate_points = apx_cb(points, max_n, False)
        lines_3 = []
        for i in range(len(generate_points)):
            lines_3.append(get_canvas_coor(generate_points[i]))

        generate_points = apx_cb(points, max_n, True)
        lines_4 = []
        for i in range(len(generate_points)):
            lines_4.append(get_canvas_coor(generate_points[i]))  

        generate_points = itp(points, max_n, alpha, False)
        lines_5 = []
        for i in range(len(generate_points)):
            lines_5.append(get_canvas_coor(generate_points[i]))

        generate_points = itp(points, max_n, alpha, True)
        lines_6 = []
        for i in range(len(generate_points)):
            lines_6.append(get_canvas_coor(generate_points[i]))           

        
while gui.running:
    event = None
    
    if gui.get_event():
        event = gui.event
    if event:
        # clear screen
        if event.key == KEY_CLEAR:
            points = []
            canvas_points = []
            lines_1 = []
            lines_2 = []
            lines_3 = []
            lines_4 = []
            lines_5 = []
            lines_6 = []
        # add point
        if event.key == ti.GUI.LMB and event.type == ti.GUI.PRESS:
            # choose one point to move
            mouse_x, mouse_y = gui.get_cursor_pos()
            current_coor = get_coordinates([mouse_x, mouse_y])
            min_distance = 100
            min_id = -1
            for i in range(len(points)):
                dist = np.linalg.norm(np.array(points[i]) - np.array(current_coor)).item()
                if ( dist < min_distance ):
                    min_id = i
                    min_distance = dist
            if min_distance < EPS:
                chosen_point_id = min_id
                print("choose point", min_id)
        if event.key == ti.GUI.LMB and event.type == ti.GUI.RELEASE:
            if chosen_point_id != -1:
                mouse_x, mouse_y = gui.get_cursor_pos()
                canvas_points[chosen_point_id] = [mouse_x, mouse_y]
                points[chosen_point_id] = get_coordinates([mouse_x, mouse_y])
                chosen_point_id = -1
                compute_and_draw()
        if event.key == ti.GUI.RMB and event.type == ti.GUI.RELEASE:
            mouse_x, mouse_y = gui.get_cursor_pos()
            canvas_points.append([mouse_x, mouse_y])
            points.append(get_coordinates([mouse_x, mouse_y]))
            compute_and_draw()
    draw() 
    gui.text("[1,2)----- Chaikin (opening)",(0.01, 0.95), 24, color=color_tab[0])   
    gui.text("[2,3)----- Chaikin (closed)",(0.01, 0.90), 24, color=color_tab[1]) 
    gui.text("[3,4)----- Cubic (opening)",(0.01, 0.85), 24, color=color_tab[2]) 
    gui.text("[4,5)----- Cubic (closed)",(0.01, 0.80), 24, color=color_tab[3]) 
    gui.text("[5,6)----- 4-P Interpolation (opening)",(0.01, 0.75), 24, color=color_tab[4]) 
    gui.text("[6,7)----- 4-P Interpolation (closed)",(0.01, 0.70), 24, color=color_tab[5]) 
    gui.show()    