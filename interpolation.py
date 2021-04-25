from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

def graphic(x_list, y_list, coeficients = [0, 0, 0, 0]):
    
    a = coeficients[0]
    b = coeficients[1]
    c = coeficients[2]
    

    if(len(x_list) == 3):    
        xvals = np.linspace(min(x_list), max(x_list), 50)
        yvals = a*xvals**2 + b*xvals + c
    
    elif(len(x_list) == 4):
        d = coeficients[3]
            
        xvals = np.linspace(min(x_list), max(x_list), 50)
        yvals = a*xvals**3 + b*xvals**2 + c*xvals + d  
    else:
        xvals = x_list
        yvals = y_list
    
    plt.plot(xvals, yvals)
    plt.scatter(x_list, y_list)
    plt.ylim(0)
    plt.stem(xvals, yvals)
    plt.show()
    
def interpolate_3points(x_list, y_list):
    
    A = np.array([[0, 0, 0]])
    B = np.array(y_list)
    
    for x in x_list:
        row = [1, x, x**2]
        A = np.append(A, [row], axis = 0)

    A = np.delete(A, (0), axis=0)
    
    x = np.linalg.solve(A, B)
    
    return np.flipud(x) 

def interpolate_4points(x_list, y_list):
    
    A = np.array([[0, 0, 0, 0]])
    B = np.array(y_list)
    
    for x in x_list:
        row = [1, x, x**2, x**3]
        A = np.append(A, [row], axis = 0)

    A = np.delete(A, (0), axis=0)
    
    x = np.linalg.solve(A, B)
    
    return np.flipud(x)

def interpolate_lagrange(m, x, y, z):
    r = 0
    
    for i in range(1, m):
        c, d = 1, 1
        for j in range(1, m):
            if i!=j:
                c = c * (z - x[j])
                d = d * (x[i] - x[j])
                   
        r = r + y[i] * c / d   
    
    return r

def spline_cubic(x_list, y_list):

    x_points = np.linspace(min(x_list), max(x_list), 10)
    
    tck = interpolate.splrep(x_list, y_list)
    
    y_points = np.array([])
    for i in x_points:
        y_points = np.append(y_points, interpolate.splev(i, tck))

    points = []
    for x, y in zip(x_points, y_points):
        points.append((x, y))
        
    return x_points, y_points
    
x = [14, 20, 25]
y = [6, 3, 2]

point1, point2, point3, point4, point5, point6, point7 = (0, 14), (7.5, 13), (15, 12), (19.5, 11), (24, 10), (30, 8), (36, 6)

point1, point2, point3, point4 = (0, 0.3), (1, 0.2), (1.3, 0.2), (1.41, 0.1)

#coord = [(x1, x2, x3, x4) for (x1, x2, x3, x4) in zip(point1, point3, point4, point7)]

coord = [(x1, x2, x3, x4) for (x1, x2, x3, x4) in zip(point1, point2, point3, point4)]
    
x, y = coord[0], coord[1]

print(x, y)
if __name__ == '__main__':
    
    
    print(spline_cubic(x, y))
    
    #print(interpolate_3points(x, y))
    #graphic(spline_cubic(x, y)[0], spline_cubic(x, y)[1])
    
    plt.plot(spline_cubic(x, y)[0], spline_cubic(x, y)[1])
    plt.plot(x, y, color = 'red')
    plt.scatter(spline_cubic(x, y)[0], spline_cubic(x, y)[1], color = 'red')
    plt.scatter(x, y, color = 'red')
    plt.ylim(0)
    plt.stem(spline_cubic(x, y)[0], spline_cubic(x, y)[1])
    plt.show()