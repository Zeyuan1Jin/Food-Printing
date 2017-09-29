import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

def picking(file, slot):
#     if if_lift:
#         file.write("G01 ")
    if slot == 2:
        file .write('G01 X45 Y30 Z8 F10000\n')
        file.write('G01 Y10 Z8\n')
        file.write('G01 Y10 Z11\n')
        file.write('G01 Y1 Z11\n')
        file.write('G01 Y1 Z15\n')
        file.write('G01 Y6 Z25\n')
        file.write('G01 Y30 Z25\n')
        
    elif slot == 3:
        file .write('G01 X87.5 Y30 Z8 F10000\n')
        file.write('G01 Y10 Z8\n')
        file.write('G01 Y10 Z11\n')
        file.write('G01 Y1 Z11\n')
        file.write('G01 Y1 Z15\n')
        file.write('G01 Y6 Z25\n')
        file.write('G01 Y30 Z25\n')
        
    elif slot == 4:
        file .write('G01 X130 Y30 Z8 F10000\n')
        file.write('G01 Y10 Z8\n')
        file.write('G01 Y10 Z11\n')
        file.write('G01 Y1 Z11\n')
        file.write('G01 Y1 Z15\n')
        file.write('G01 Y6 Z25\n')
        file.write('G01 Y30 Z25\n')
    
def dropping(file, slot):
#     if if_lift:
#         file.write()
        if slot == 2:
            file.write('G01 X45 Y30 Z26 E0.0 F4000\n')
            file.write('G01 Y5 Z26\n')
            file.write('G01 Y2 Z26\n')
            file.write('G01 Y2 Z9\n')
            file.write('G01 Y30 Z9\n')

        elif slot == 3:
            file.write('G01 X87.5 Y30 Z26 E0.0 F4000\n')
            file.write('G01 Y5 Z26\n')
            file.write('G01 Y2 Z26\n')
            file.write('G01 Y2 Z9\n')
            file.write('G01 Y30 Z9\n')
            
        elif slot == 4:
            file.write('G01 X130 Y30 Z26 E0.0 F4000\n')
            file.write('G01 Y5 Z26\n')
            file.write('G01 Y2 Z26\n')
            file.write('G01 Y2 Z9\n')
            file.write('G01 Y30 Z9\n')
# def final_cooking(file, time, x_center, y_center):
    

class material:
    travel_speed = 6000 
    
    def __init__(self, print_speed, slot, dump, if_outer, color):
#         self.multi = extrusion_multi
        self.speed = print_speed
        self.slot = slot
        self.dump = 10 + dump # initial value to be adjust
        self.if_outer = if_outer
        self.x_trace = []
        self.y_trace = []
        self.z_trace = []
        self.color = color
        
    def pick(self, file):
        picking(file, self.slot)
    
    def drop(self, file):
        dropping(file, self.slot)
        
    def extrude(self, file, twist_angle, size, layer, z, spacing, spacing_o, unit_E, x_center, y_center, ax):
        x = []
        y = []
        e = [0]
        e_true = [0]
        
        t = list(range(4))
        t = [i * 2 * np.pi/3 + twist_angle for i in t]
        
        
        if self.if_outer:
            if layer > 19:
                walls = 1
            else:
                walls = 2
            # condition to reduce the walls to 1
        else:
#             if size // spacing - int(size // spacing) == 0:
            size = size - 2 * spacing_o
            walls = int(size // spacing)
            if walls == 0:
                walls = 1
#             else: 
#                 walls = int(size // spacing) + 1

        for j in range(walls):
            x.extend([x_center + (size * 2 / 3**0.5 - 2 / 3**0.5*j*spacing)*np.cos(i) for i in t])
            y.extend([y_center + (size * 2 / 3**0.5 - 2/ 3**0.5*j*spacing)*np.sin(i) for i in t])

        for k in range(walls):
            for l in range(len(t) - 1):
                e.append(unit_E * ((x[k * len(t) + l + 1] - x[k * len(t) + l]) ** 2 +\
                (y[k * len(t) + l + 1] - y[k * len(t) + l]) ** 2) ** 0.5)


        for k in range(len(e) - 1):
            e[k + 1] = e[k + 1] + e[k]

        for k in range(walls - 1):
            e_true.extend(e[k * (len(t) - 1) + 1 : (k+1) * (len(t) - 1) + 1])
            e_true.append(e[(k + 1) * (len(t) - 1)])

        e_true.extend(e[(walls - 1) * (len(t) - 1) + 1:])
        e_true = [i + self.dump for i in e_true]
        self.dump = e_true[-1]

        file.write('G01 X%4.2f Y%4.2f Z%4.2f E%4.2f F%4.2f\n'%(x[0], y[0], z, e_true[0], self.travel_speed))
        for i in range(1, len(x)):
            file.write('G01 X%4.2f Y%4.2f Z%4.2f E%4.2f F%4.2f\n'%(x[i], y[i], z, e_true[i], self.speed))
        
        if self.if_outer:
            ax.plot(x, y, z, linewidth = '8', color = self.color, alpha = 0.5)
        ax.plot(x, y, z, linewidth = '8', color = self.color)
    
    def cook(self, file, height, z, layer, twist_angle, size, spacing, cook_speed, x_center, y_center):
        temp = 255
        
        x = []
        y = []
        
        t = list(range(4))
        t = [i * 2 * np.pi/3 + twist_angle for i in t]
        
        cook_off_set = -60
        
        if self.if_outer:
            if layer > 19:
                x.extend([x_center + size * 2 / 3**0.5 * np.cos(i) for i in t])
                y.extend([y_center + size * 2 / 3**0.5 * np.sin(i) + cook_off_set  for i in t])
            else:
                x.extend([x_center + (size * 2/ 3**0.5 - 2/ 3**0.5*0.5*spacing)*np.cos(i) for i in t])
                y.extend([y_center + (size * 2/ 3**0.5 - 2/ 3**0.5*0.5*spacing)*np.sin(i) + cook_off_set for i in t])
        else:
            x.extend([x_center + (size * 2/ 3**0.5 - 2/3**0.5*2*spacing)*np.cos(i)*0.7 for i in t])
            y.extend([y_center + (size * 2/ 3**0.5 - 2/ 3**0.5*2*spacing)*np.sin(i)*0.7 + cook_off_set for i in t])
        
        file.write('G01 X%4.2f Y%4.2f Z%4.2f F%4.2f\n'%(x[0], y[0], z + height, self.travel_speed))
        file.write('M106 S%4.2f\n'%temp)
        for i in range(1, len(x)):
            file.write('G01 X%4.2f Y%4.2f Z%4.2f F%4.2f\n'%(x[i], y[i], z + height, cook_speed))
        if not self.if_outer:
            file.write('G01 X%4.2f Y%4.2f Z%4.2f F%4.2f\n'%(x_center, y_center + cook_off_set, z + height, self.travel_speed))
            time = 5000 + 10000 * (25 - layer) // 25
            file.write('G04 P%s\n'%time)
            file.write('M106 S0.00\n')
        elif layer > 19:
            file.write('M106 S0.00\n')
            
    def test_extrude(self,file):
            file.write('G01 X20 Y140 Z25\n')
            file.write('G01 E%4.2f F1200\n'%self.dump)


def food(filename):
    nozzel_dia = 1.77
    syringe_dia = 22.5
    extrusion_width = 1.5 * nozzel_dia
    extrusion_multi = 1.0
    # to be set
    retraction = 3
    retraction_speed = 400
    
    num_layers = 25
    size = 21
    twist_angle = np.deg2rad(3)
    layer_to_fill = 15
    z_bed = 12

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x_base = np.linspace(110, 170, 50)
    y_base = np.linspace(110, 170, 50)
    x_base, y_base = np.meshgrid(x_base, y_base)
    z_base = np.zeros((50, 50))
    ax.plot_surface(x_base, y_base, z_base + z_bed, color = '#d1d1e0')
    
    outer = material(1200, 2, 58, if_outer = True, color = 'k')
    outer_first = True
    cook_outer = True
    out_height = 1.6
    spacing_o = extrusion_width - out_height * (1 - np.pi / 4)
    unit_Eo = extrusion_multi * ((extrusion_width - out_height) * out_height +\
        np.pi * (out_height / 2) ** 2) / (np.pi * (syringe_dia / 2) ** 2)
    
    material_1 = material(1200, 3, 38, if_outer = False, color = 'w')
    m1_first = True
    layer1_height = 1.3
    spacing_1 = extrusion_width - layer1_height * (1 - np.pi / 4)
    unit_E1 = extrusion_multi * ((extrusion_width - layer1_height) * layer1_height +\
        np.pi * (layer1_height / 2) ** 2) / (np.pi * (syringe_dia / 2) ** 2)
    
    material_2 = material(1200, 4, 48, if_outer = False, color = 'y')
    m2_first = True
    layer2_height = 1.3
    # conpen2_height = 0.1 # + factor2 * layer
    spacing_2 = extrusion_width - layer2_height * (1 - np.pi / 4)
    unit_E2 = extrusion_multi * ((extrusion_width - layer2_height) * layer2_height +\
        np.pi * (layer2_height / 2) ** 2) / (np.pi * (syringe_dia / 2) ** 2)
    
    x_center = 140
    y_center = 140
    
    #initialize the file
    filename = filename + '.gcode'
    file = open(filename, 'w')
    file.write('G21\n')
    file.write('G90\n')
    file.write('M82\n')
    file.write('G01 F6000\n')
    file.write('T0\n')
    file.write('G92 E0\n')
    file.write('G28 Z\n')
    # to be notice, first home z then home x, y for hardware consideration
    file.write('G28 X Y\n')

    z = z_bed
    for i in range(layer_to_fill):
        if i % 2 == 0:
            conpen1_height = 0.3 # + factor2 * layer
            z = z + layer1_height + conpen1_height
            outer.pick(file)
            
            if outer_first:
                outer.test_extrude(file)
                outer_first = False
        
            size_layer = size * (num_layers - i) / num_layers
            outer.extrude(file, twist_angle * i, size_layer, i, z, spacing_o, spacing_o, unit_Eo, 140, 140, ax)
            outer.drop(file)
            material_1.pick(file)
            if m1_first:
                material_1.test_extrude(file)
                m1_first = False
                
            material_1.extrude(file, twist_angle * i, size_layer, i, z, spacing_1, spacing_o, unit_Eo, 140, 140, ax)
            material_1.drop(file)
            if cook_outer:
#  file, height, z, layer, twist_angle, size, spacing, temp, cook_speed
                outer.cook(file, 10, z, i, twist_angle * i, size_layer, spacing_1, 200, 140, 140)
            material_1.cook(file, 10, z, i, twist_angle * i, size_layer, spacing_1, 200, 140, 140)
        else:
            conpen2_height = 0.3 # + factor2 * layer
            z = z + layer2_height + conpen2_height
            outer.pick(file)
            size_layer = size * (num_layers - i) / num_layers
            outer.extrude(file, twist_angle * i, size_layer,i, z, spacing_o, spacing_o, unit_E2, 140, 140, ax)
            
            outer.drop(file)
            material_2.pick(file)
            if m2_first:
                material_2.test_extrude(file)
                m2_first = False
                
            material_2.extrude(file, twist_angle * i, size_layer, i, z, spacing_2, spacing_o, unit_E2, 140, 140, ax)
            material_2.drop(file)
            if cook_outer:
                outer.cook(file, 10, z, i, twist_angle * i, size_layer, spacing_2, 200, 140, 140)
            material_2.cook(file, 10, z, i, twist_angle * i, size_layer, spacing_2, 200, 140, 140)
    
    outer.pick(file)
    for i in range(layer_to_fill, num_layers):
        
        z = z + layer1_height + conpen1_height
        size_layer = size * (num_layers - i) / num_layers
        outer.extrude(file, twist_angle * i, size_layer, i, z, spacing_o, spacing_o, unit_E1, 140, 140, ax)
#         retract
    outer.cook(file, 10, z, i, twist_angle * i, size_layer, spacing_1, 200, 140, 140)
    file.close()

    ax.set_xlim(110, 170)
    ax.set_ylim(110, 170)
    area = syringe_dia ** 2 * np.pi / 4
    ax.text(110, 110, 65, "Sesame:%.2fcc"%((outer.dump - 58)*area/1000), color = 'k')
    ax.text(110, 110, 55, "Chicken:%.2fcc"%((material_2.dump - 48)*area/1000), color = 'y')
    ax.text(110, 110, 60, "Shrimp:%.2fcc"%((material_1.dump - 38)*area/1000), color = '#d1d1e0')
    ax.axis('off')
    plt.show()
    



food('test')