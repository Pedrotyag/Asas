import numpy as np
import interpolation

class section:
    def __init__(self,  chord1, chord2, coord_root, semib):
        
         self.chord1 = max(chord1, chord2)
         self.mid_chord = (chord1 + chord2) * 0.8 / 2
         self.chord2 = min(chord1, chord2)
         
         self.coord_root = coord_root
         self.coord_mid = (coord_root[0] + semib/2, self.mid_chord)
         self.coord_tip = (coord_root[0] + semib, chord2)
    
    def file(self): # Não mexer nisso~

        x = "SECTION                                                     |  (keyword)\n" + "%f   %f    0.0000    %f   0.000   13    1   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %(0,  self.coord_tip[0], self.chord2)+ "AFIL 0.0 1.0\n"+ "airfoil.dat \n"
        
        return x
        


def quadratic_suavization_section(section_object): 
    
    point1, point2, point3 = section_object.coord_root, section_object.coord_mid, section_object.coord_tip
    
    coord = [(x1, x2, x3) for (x1, x2, x3) in zip(point1, point2, point3)]
    
    x, y = coord[0], coord[1]
    
    coeficients_quadratic = interpolation.interpolate_3points(x, y)
    
    return section_object.file()
    

def cubic_smoothing_section(x_list, y_list, section_object = 0):
    
    '''
    for i in range(4):
        section_wing = section_object()
    '''
    
    coeficients_cubic = interpolation.interpolate_4points(x_list, y_list)
    
    
    a = coeficients_cubic[0]
    b = coeficients_cubic[1]
    c = coeficients_cubic[2]
    d = coeficients_cubic[3]
    
    x = np.linspace(min(x_list), max(x_list), 10)
    
    y = a*x**3 + b*x**2 + c*x + d
    
    return x, y
    
def cubic_spline_smoothing_section(x_list, y_list):
    
    x, y = interpolation.spline_cubic(x_list, y_list)



point1, point2, point3, point4, point5, point6, point7 = (0, 14), (7.5, 13), (15, 12), (19.5, 11), (24, 10), (30, 8), (36, 6)

coord = [(x1, x2, x3, x4, x5, x6, x7) for (x1, x2, x3, x4, x5, x6, x7) in zip(point1, point2, point3, point4, point5, point6, point7)]
    
x, y = coord[0], coord[1]


chord1 = 14
chord2 = 12
coord_root = (0, 14)
semib = 15

section = section(chord1, chord2, coord_root, semib)

with open('section.avl', 'w') as o:
    o.write(quadratic_suavization_section(section))


x = [0, 14, 20, 25]
y = [8, 6, 3, 2]



#cubic_suavization_section(x, y)
