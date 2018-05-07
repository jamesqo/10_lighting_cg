import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 8

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    amb = calculate_ambient(ambient, areflect)
    diff = calculate_diffuse(light, dreflect, normal)
    spec = calculate_specular(light, sreflect, view, normal) 
    color = [x + y + z for x, y, z in zip(amb, diff, spec)]
    return limit_color(color)

def calculate_ambient(alight, areflect):
    color = [x * y for x, y in zip(alight, areflect)]
    return limit_color(color)

def calculate_diffuse(light, dreflect, normal):
    color = [x * y * dot_product(normalize(normal), normalize(light[LOCATION])) for x, y in zip(light[COLOR], dreflect)]
    return limit_color(color)

def calculate_specular(light, sreflect, view, normal):
    a = dot_product(normalize(normal), normalize(light[LOCATION]))
    color = [0, 0, 0]
    if a > 0:
        b = [2 * a * x - y for x, y in zip(normalize(normal), normalize(light[LOCATION]))]
        R = dot_product(b, normalize(view)) ** SPECULAR_EXP
        color = [x * y * R for x, y in zip(light[COLOR], sreflect)]
    return limit_color(color)

def limit_color(color):
    return [255 if x > 255 else 0 if x < 0 else int(x) for x in color]

#vector functions
def normalize(vector):
    magnitude = math.sqrt(dot_product(vector, vector))
    return [x / magnitude for x in vector]

def dot_product(a, b):
    return sum([x * y for x, y in zip(a, b)])

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N