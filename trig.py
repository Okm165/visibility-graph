from functools import cmp_to_key
from math import sqrt
from graph import Vertex


ZERO_TOLERANCE = 10**(-6)

def ccw(A, B, C):
    """ Return 1 if counter clockwise, -1 if clock wise, 0 if collinear """
    det = (A.x-C.x) * (B.y-C.y) - (B.x-C.x) * (A.y-C.y)
    if det > ZERO_TOLERANCE:
        return 1
    elif det < -ZERO_TOLERANCE:
        return -1
    return 0


def on_segment(p, q, r):
    """ Given three colinear points p, q, r, the function checks if point q lies on line segment 'pr'. """
    if (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)):
        if (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)):
            return True
    return False


def edge_intersect(edge1, edge2):
    """ Return True if edge1 interects edge2. """
    o1 = ccw(edge1.v1, edge1.v2, edge2.v1)
    o2 = ccw(edge1.v1, edge1.v2, edge2.v2)
    o3 = ccw(edge2.v1, edge2.v2, edge1.v1)
    o4 = ccw(edge2.v1, edge2.v2, edge1.v2)

    # General case
    if (o1 != o2 and o3 != o4):
        return True
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if o1 == 0 and on_segment(edge1.v1, edge2.v1, edge1.v2):
        return True
    # p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if o2 == 0 and on_segment(edge1.v1, edge2.v2, edge1.v2):
        return True
    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if o3 == 0 and on_segment(edge2.v1, edge1.v1, edge2.v2):
        return True
    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if o4 == 0 and on_segment(edge2.v1, edge1.v2, edge2.v2):
        return True
    return False


def distance(v1, v2):
    """ Return the Euclidean distance between two vertices. """
    return sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2)


def unit_vector(v1, v2):
    """ Normalize vector between vector v1 and v2 """
    magnitude = distance(v1, v2)
    return Vertex((v2.x - v1.x) / magnitude, (v2.y - v1.y) / magnitude)

def cmp_angles(O, A, B):
    """ Compare relative angle wrt to O, A to B """
    return ccw(B, A, O)

def cmp_distance(O, A, B):
    """ Compare relative distance wrt to O, A to B """
    d_OA = distance(O, A)
    d_OB = distance(O, B)

    if d_OA - d_OB > ZERO_TOLERANCE:
        return 1
    elif d_OA - d_OB < -ZERO_TOLERANCE:
        return -1
    return 0 

def cmp_angle_distance(O, A, B):
    """ Sort by relative angle and relative distance from O vertex perspective """
    cmp = cmp_angles(O, A, B)
    if cmp != 0: return cmp
    else: return cmp_distance(O, A, B)

def cmp_angle_distance_factory(O):
    """ Creates function that has O vertex encoded inside, useful for sorting function """
    return lambda A, B: cmp_angle_distance(O ,A ,B)

def sort_by_angle_distance(O, verts):
    """ Returns vertecies sorted by angle from O vertex perspective"""
    return sorted(verts, key=cmp_to_key(cmp_angle_distance_factory(O)))
