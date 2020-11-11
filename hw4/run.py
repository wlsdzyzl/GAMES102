import taichi as ti
import numpy as np
import parameterization as pr
from cubic_spline import cubic_spline
from bezier import bezier
from bezier import bezier_interpolator
# use taichi to visualize the fitting results
cs_x = cubic_spline()
cs_y = cubic_spline()
bz = bezier()
bzi = bezier_interpolator()
points = []
EPS = 0.1
# draw on canvas
canvas_points = []
# boundary = 0
lines_1 = []
# boundary = 1
lines_2 = []
# g1 same direction and same norm 
lines_3 = []
# g1 same direction and different norm
lines_4 = []
# g1 different direction
lines_5 = []
# bezier
lines_6 = []
# bezier interpolation
lines_7 = []

res = (800, 600)
x_range = [-4, 4]
y_range = [-3, 3]
t_range = [0, 1]
t_len = t_range[1] - t_range[0]
x_len = x_range[1] - x_range[0]
y_len = y_range[1] - y_range[0]
p_m = 1
color_tab = [0x1f77b4, 0xff7f0e, 0x2ca02c, 0xd62728, 0x9467bd, 0x8c564b, 0xe377c2, 0x7f7f7f, 0xbcbd22, 0x17becf]
chosen_point_id = -1
def get_coordinates(p):
    return [x_range[0] +  p[0] * x_len, y_range[0] + p[1] * y_len]

def get_canvas_coor(p):
    return [(p[0] - x_range[0]) / x_len, ( p[1] - y_range[0]) / y_len ]

# use gui to generate points
gui = ti.GUI("Cubic Spline", res)
# add slide
selector = gui.slider('selector', 1, 8.99, step=1)
# add button 
KEY_CLEAR = gui.button('clear')


def draw():
    # draw points
    for p in canvas_points:
        gui.circle(p, 0xFF0000, 8)
    # draw lines
    r = 1.5
    selector_value = int(selector.value)

    if selector_value == 1 or selector_value == 8:
        for i in range(len(lines_1) - 1):
            gui.line(lines_1[i], lines_1[i+1], color=color_tab[0], radius= r)
    if selector_value == 2 or selector_value == 8:
        for i in range(len(lines_2) - 1):
            gui.line(lines_2[i], lines_2[i+1], color=color_tab[1], radius = r) 
    if selector_value == 3 or selector_value == 8:
        for i in range(len(lines_3) - 1):
            gui.line(lines_3[i], lines_3[i+1], color=color_tab[2], radius = r)    
    if selector_value == 4 or selector_value == 8:
        for i in range(len(lines_4) - 1):
            gui.line(lines_4[i], lines_4[i+1], color=color_tab[3], radius = r) 
    
    if selector_value == 5 or selector_value == 8:
        for i in range(len(lines_5) - 1):
            gui.line(lines_5[i], lines_5[i+1], color=color_tab[4], radius = r)
    if selector_value == 6 or selector_value == 8:
        for i in range(len(lines_6) - 1):
            gui.line(lines_6[i], lines_6[i+1], color=color_tab[5], radius = r)    
    if selector_value == 7 or selector_value == 8:
        for i in range(len(lines_7) - 1):
            gui.line(lines_7[i], lines_7[i+1], color=color_tab[6], radius = r)  
        for i in range(len(bzi.beziers)):
            for p in bzi.beziers[i].points:
                gui.circle( get_canvas_coor(p), color = color_tab[-1], radius=4)

def compute_and_draw():
    global points
    global p_m
    global lines_1
    global lines_2
    global lines_3
    global lines_4
    global lines_5
    global lines_6
    global lines_7
    if len(points)>= 3:
        if p_m == 0:
            t = pr.uniform(np.array(points))
        if p_m == 1:
            t = pr.chordal(np.array(points))
        if p_m == 2:
            t = pr.centripetal(np.array(points))
        if p_m == 3:
            t = pr.foley(np.array(points))
        t = [tmp * t_len + t_range[0] for tmp in t]
    
        tx = []
        ty = []
        for i in range(len(t)):
            tx.append([t[i], points[i][0]])
            ty.append([t[i], points[i][1]])
        # use polynomial interpolation
        cs_x.set_points(tx)
        cs_y.set_points(ty)
        bz.set_control_points(points)
        bzi.set_points(points)
        bzi.set_parameter(t)
        cs_x.construct_cubic_spline(0)
        cs_y.construct_cubic_spline(0)
        t_axis = np.linspace(t_range[0], t_range[1], 500)
        
        x_axis = [cs_x.new_points(tmp_t) for tmp_t in t_axis]
        y_axis = [cs_y.new_points(tmp_t) for tmp_t in t_axis]

        # get_canvas_coor to transform points into canvas
        lines_1 = []
        for i in range(len(t_axis)):
            lines_1.append(get_canvas_coor([x_axis[i], y_axis[i]]))

        cs_x.construct_cubic_spline(1)
        cs_y.construct_cubic_spline(1)

        # boundary = 1
        
        x_axis = [cs_x.new_points(tmp_t) for tmp_t in t_axis]
        y_axis = [cs_y.new_points(tmp_t) for tmp_t in t_axis]

        # get_canvas_coor to transform points into canvas
        lines_2 = []
        for i in range(len(t_axis)):
            lines_2.append(get_canvas_coor([x_axis[i], y_axis[i]]))
        
        # g1 0
        cs_x.construct_cubic_spline_g1_0(10)
        cs_y.construct_cubic_spline_g1_0(10)        
        
        
        x_axis = [cs_x.new_points(tmp_t) for tmp_t in t_axis]
        y_axis = [cs_y.new_points(tmp_t) for tmp_t in t_axis]

        # get_canvas_coor to transform points into canvas
        lines_3 = []
        for i in range(len(t_axis)):
            lines_3.append(get_canvas_coor([x_axis[i], y_axis[i]]))    

        # g1 1
        cs_x.construct_cubic_spline_g1_1(10)
        cs_y.construct_cubic_spline_g1_1(10)        
        
        
        x_axis = [cs_x.new_points(tmp_t) for tmp_t in t_axis]
        y_axis = [cs_y.new_points(tmp_t) for tmp_t in t_axis]

        # get_canvas_coor to transform points into canvas
        lines_4 = []
        for i in range(len(t_axis)):
            lines_4.append(get_canvas_coor([x_axis[i], y_axis[i]]))              
          
        # g1 0
        cs_x.construct_cubic_spline_g1_1(-5)
        cs_y.construct_cubic_spline_g1_1(-5)        
        
        
        x_axis = [cs_x.new_points(tmp_t) for tmp_t in t_axis]
        y_axis = [cs_y.new_points(tmp_t) for tmp_t in t_axis]

        # get_canvas_coor to transform points into canvas
        lines_5 = []
        for i in range(len(t_axis)):
            lines_5.append(get_canvas_coor([x_axis[i], y_axis[i]]))  

        # bezier    
        # get_canvas_coor to transform points into canvas
        lines_6 = []
        for i in range(len(t_axis)):
            tmp_p = bz.deCasteljau(t_axis[i])
            lines_6.append(get_canvas_coor([tmp_p[0], tmp_p[1]]))    

        # bezier_interpolation
        # get_canvas_coor to transform points into canvas
        lines_7 = []
        for i in range(len(t_axis)):
            tmp_p = bzi.deCasteljau(t_axis[i])
            lines_7.append(get_canvas_coor([tmp_p[0], tmp_p[1]]))         
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
            lines_7 = []
            bzi.beziers = []
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
    if p_m == 0:
        gui.text("using uniform parameterization",(0.01, 0.99), 24)
    if p_m == 1:
        gui.text("using chordal parameterization",(0.01, 0.99), 24)
    if p_m == 2:
        gui.text("using centripetal parameterization",(0.01, 0.99), 24)
    if p_m == 3:
        gui.text("using foley parameterization",(0.01, 0.99), 24)   
    gui.text("[1,2)----- Natural Spline",(0.01, 0.95), 24, color=color_tab[0])   
    gui.text("[2,3)----- End Slope Spline",(0.01, 0.90), 24, color=color_tab[1]) 
    gui.text("[3,4)----- G1-0",(0.01, 0.85), 24, color=color_tab[2]) 
    gui.text("[4,5)----- G1-1",(0.01, 0.80), 24, color=color_tab[3]) 
    gui.text("[5,6)----- G0",(0.01, 0.75), 24, color=color_tab[4]) 
    gui.text("[6,7)----- Bezier",(0.01, 0.70), 24, color=color_tab[5]) 
    gui.text("[7,8)----- Bezier Interpolation",(0.01, 0.65), 24, color=color_tab[6])
    gui.text("control points of Bezier Interpolation",(0.01, 0.60), 24, color=color_tab[-1])
    gui.show()    