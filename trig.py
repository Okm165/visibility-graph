from functools import cmp_to_key
from math import sqrt
from graph import Vertex, Edge


ZERO_TOLERANCE = 10**(-6)


def ccw(A: Vertex, B: Vertex, C: Vertex):
    """ Return 1 if counter clockwise, -1 if clock wise, 0 if collinear """
    det = (A.x-C.x) * (B.y-C.y) - (B.x-C.x) * (A.y-C.y)
    if det > ZERO_TOLERANCE:
        return 1
    elif det < -ZERO_TOLERANCE:
        return -1
    return 0


def on_segment(p: Vertex, q: Vertex, r: Vertex):
    """ Given three colinear points p, q, r, the function checks if point q lies on line segment 'pr'. """
    if (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)):
        if (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)):
            return True
    return False


def edge_intersect(edge1: Edge, edge2: Edge):
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


def distance(v1: Vertex, v2: Vertex):
    """ Return the Euclidean distance between two vertices. """
    return sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2)


def unit_vector(v1: Vertex, v2: Vertex):
    """ Normalize vector between vector v1 and v2 """
    magnitude = distance(v1, v2)
    return Vertex((v2.x - v1.x) / magnitude, (v2.y - v1.y) / magnitude)


def cmp_angles(O: Vertex, A: Vertex, B: Vertex):
    """ Compare relative angle wrt to O, A to B """
    return ccw(B, A, O)


def cmp_distance(O: Vertex, A: Vertex, B: Vertex):
    """ Compare relative distance wrt to O, A to B """
    d_OA = distance(O, A)
    d_OB = distance(O, B)

    if d_OA - d_OB > ZERO_TOLERANCE:
        return 1
    elif d_OA - d_OB < -ZERO_TOLERANCE:
        return -1
    return 0


def cmp_angle_distance(O: Vertex, A: Vertex, B: Vertex):
    """ Sort by relative angle and relative distance from O vertex perspective """
    cmp = cmp_angles(O, A, B)
    if cmp != 0:
        return cmp
    else:
        return cmp_distance(O, A, B)


def cmp_angle_distance_factory(O: Vertex):
    """ Creates function that has O vertex encoded inside, useful for sorting function """
    return lambda A, B: cmp_angle_distance(O, A, B)


def sort_by_angle_distance(O: Vertex, verts: list):
    """ Returns vertecies sorted by angle from O vertex perspective """
    return sorted(verts, key=cmp_to_key(cmp_angle_distance_factory(O)))


def edge_intersect_vertex(e1: Edge, e2: Edge) -> Vertex | None:
    """ Return intersect Vertex where the edge e1 crosses e2 if not crossing None """
    tdiv = (e1.s.x-e1.e.x)*(e2.s.y-e2.e.y)-(e1.s.y-e1.e.y)*(e2.s.x-e2.e.x)
    if tdiv == 0:
        return None

    t = ((e1.s.x-e2.s.x)*(e2.s.y-e2.e.y)-(e1.s.y-e2.s.y)*(e2.s.x-e2.e.x)) / tdiv
    if not 0 <= t or not t <= 1:
        return None

    u = ((e1.s.x-e2.s.x)*(e1.s.y-e1.e.y)-(e1.s.y-e2.s.y)*(e1.s.x-e1.e.x)) / tdiv
    if not 0 <= u or not u <= 1:
        return None

    return Vertex(e1.s.x+t*(e1.e.x-e1.s.x), e1.s.y+t*(e1.e.y-e1.s.y))


def edge_distance(e1: Edge, e2: Edge) -> int:
    """ Returns distance from begining of e1 to intersection of e1 and e2 """
    v = edge_intersect_vertex(e1, e2)
    if v is not None:
        return distance(e1.v1, v)
    return 0


def cmp_edges(p: Edge, e1: Edge, e2: Edge):
    """ Compare e1 to e2 relative to edge p """
    if e1 == e2:
        return 0
    if not edge_intersect(p, e2):
        return 1
    d_p_e1 = edge_distance(p, e1)
    d_p_e2 = edge_distance(p, e2)
    if d_p_e1 - d_p_e2 > ZERO_TOLERANCE:
        return -1
    elif d_p_e1 - d_p_e2 < -ZERO_TOLERANCE:
        return 1
    else:
        # if distances are equal compare slopes
        uv_e1 = unit_vector(e1.v1, e1.v2)
        uv_e2 = unit_vector(e2.v1, e2.v2)
        s = cmp_angles(Vertex(0, 0), uv_e1, uv_e2)
        if s > ZERO_TOLERANCE:
            return -1
        elif s < -ZERO_TOLERANCE:
            return 1
        else:
            # if slopes are equal compare lengths
            l_e1 = distance(e1.v1, e1.v2)
            l_e2 = distance(e2.v1, e2.v2)
            if l_e1 - l_e2 > ZERO_TOLERANCE:
                return -1
            elif l_e1 - l_e2 < -ZERO_TOLERANCE:
                return 1
            else:
                return 0


class EdgeSet:
    def __init__(self):
        self._edges = []

    def insert(self, p, edge):
        self._edges.insert(self._index(p, edge), edge)

    def delete(self, p, edge):
        index = self._index(p, edge) - 1
        if self._edges[index] == edge:
            del self._edges[index]

    def smallest(self):
        return self._edges[0]

    def largest(self):
        return self._edges[len(self._edges-1)]

    def _index(self, p, edge):
        lo = 0
        hi = len(self._edges)
        while lo < hi:
            mid = (lo+hi)//2
            if cmp_edges(p, edge, self._edges[mid]) < 0:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def __len__(self):
        return len(self._edges)

    def __getitem__(self, index):
        return self._edges[index]
