from graph import *
from constants import *
from math import pi, sqrt, atan, acos



def polygon_cross(v1: Vertex, poly_edges) -> bool:
    """Returns True if Vertex v1 is internal to the polygon. The polygon is
    defined by the Edges in poly_edges. Uses crossings algorithm and takes into
    account edges that are collinear to v1."""
    v2 = Vertex(INF, v1.y)
    intersect_count = 0
    for edge in poly_edges:
        if v1.y < edge.v1.y and v1.y < edge.v2.y:
            continue
        if v1.y > edge.v1.y and v1.y > edge.v2.y:
            continue
        if v1.x > edge.v1.x and v1.x > edge.v2.x:
            continue
        # Deal with Vertexs collinear to v1
        edge_v1_collinear = (ccw(v1, edge.v1, v2) == COLLINEAR)
        edge_v2_collinear = (ccw(v1, edge.v2, v2) == COLLINEAR)
        if edge_v1_collinear and edge_v2_collinear:
            continue
        if edge_v1_collinear or edge_v2_collinear:
            collinear_vertex = edge.v1 if edge_v1_collinear else edge.v2
            if edge.get_adjacent(collinear_vertex).y > v1.y:
                intersect_count += 1
        elif edge_intersect(v1, v2, edge):
            intersect_count += 1
    if intersect_count % 2 == 0:
        return False
    return True


def edge_in_polygon(v1: Vertex, v2: Vertex, graph: Graph) -> bool:
    """Return true if the edge from v1 to v2 is interior to any polygon
    in graph."""
    if v1.polygon_id != v2.polygon_id:
        return False
    if v1.polygon_id == -1 or v2.polygon_id == -1:
        return False
    mid_vertex = Vertex((v1.x + v2.x) / 2, (v1.y + v2.y) / 2)
    return polygon_cross(mid_vertex, graph.polygons[v1.polygon_id])


def unit_vector(a: Vertex, b: Vertex) -> Vertex:
    magnitude = distance(a, b)
    return Vertex((a.x - b.x) / magnitude, (a.y - b.y) / magnitude)


def distance(v1: Vertex, v2: Vertex) -> float:
    """Return the Euclidean distance between two Vertexs."""
    return sqrt((v2.x - v1.x)**2 + (v2.y - v1.y)**2)


def intersect_vertex(v1: Vertex, v2: Vertex, edge: Edge):
    """Return intersect Vertex where the edge from v1, v2 intersects edge"""
    if v1 in edge:
        return v1
    if v2 in edge:
        return v2
    if edge.v1.x == edge.v2.x:
        if v1.x == v2.x:
            return None
        pslope = (v1.y - v2.y) / (v1.x - v2.x)
        intersect_x = edge.v1.x
        intersect_y = pslope * (intersect_x - v1.x) + v1.y
        return Vertex(intersect_x, intersect_y)

    if v1.x == v2.x:
        eslope = (edge.v1.y - edge.v2.y) / (edge.v1.x - edge.v2.x)
        intersect_x = v1.x
        intersect_y = eslope * (intersect_x - edge.v1.x) + edge.v1.y
        return Vertex(intersect_x, intersect_y)

    pslope = (v1.y - v2.y) / (v1.x - v2.x)
    eslope = (edge.v1.y - edge.v2.y) / (edge.v1.x - edge.v2.x)
    if eslope == pslope:
        return None
    intersect_x = (eslope * edge.v1.x - pslope * v1.x +
                   v1.y - edge.v1.y) / (eslope - pslope)
    intersect_y = eslope * (intersect_x - edge.v1.x) + edge.v1.y
    return Vertex(intersect_x, intersect_y)


def vertex_distance(v1: Vertex, v2: Vertex, edge: Edge) -> float:
    """ return the distance from v1 to intersect Vertex with edge, 0 if no intersection """
    ip = intersect_vertex(v1, v2, edge)
    if ip is not None:
        return distance(v1, ip)
    return 0


def angle(center: Vertex, vert: Vertex):
    """ Return the angle (radian) of Vertex from center of the radian circle """
    dx = vert.x - center.x
    dy = vert.y - center.y
    if dx == 0:
        if dy < 0:
            return pi * 3 / 2
        return pi / 2
    if dy == 0:
        if dx < 0:
            return pi
        return 0
    if dx < 0:
        return pi + atan(dy / dx)
    if dy < 0:
        return 2 * pi + atan(dy / dx)
    return atan(dy / dx)


def angle2(va: Vertex, vb: Vertex, vc: Vertex) -> float:
    """Return angle B (radian) between vb and vc """
    a = (vc.x - vb.x)**2 + (vc.y - vb.y)**2
    b = (vc.x - va.x)**2 + (vc.y - va.y)**2
    c = (vb.x - va.x)**2 + (vb.y - va.y)**2
    cos_value = (a + c - b) / (2 * sqrt(a) * sqrt(c))
    return acos(int(cos_value*T)/T2)


def ccw(a: Vertex, b: Vertex, c: Vertex):
    """Return 1 if counter clockwise, -1 if clock wise, 0 if collinear """
    det = int(((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x))*T)/T2
    if det > 0:
        return 1
    if det < 0:
        return -1
    return 0


def on_segment(p: Vertex, q: Vertex, r: Vertex):
    """Given three colinear Vertexs p, q, r, the function checks if Vertex q
    lies on line segment 'pr'."""
    if (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)):
        if (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)):
            return True
    return False


def edge_intersect(v1: Vertex, q1: Vertex, edge: Edge) -> bool:
    """Return True if edge from A, B interects edge"""
    v2 = edge.v1
    q2 = edge.v2
    o1 = ccw(v1, q1, v2)
    o2 = ccw(v1, q1, q2)
    o3 = ccw(v2, q2, v1)
    o4 = ccw(v2, q2, q1)

    # General case
    if (o1 != o2 and o3 != o4):
        return True
    # v1, q1 and v2 are colinear and v2 lies on segment v1q1
    if o1 == COLLINEAR and on_segment(v1, v2, q1):
        return True
    # v1, q1 and v2 are colinear and q2 lies on segment v1q1
    if o2 == COLLINEAR and on_segment(v1, q2, q1):
        return True
    # v2, q2 and v1 are colinear and v1 lies on segment v2q2
    if o3 == COLLINEAR and on_segment(v2, v1, q2):
        return True
    # v2, q2 and q1 are colinear and q1 lies on segment v2q2
    if o4 == COLLINEAR and on_segment(v2, q1, q2):
        return True
    return False


def cmp_edges(v1: Vertex, v2: Vertex, edge1: Edge, edge2: Edge) -> float:
    """Return True if edge1 is smaller than edge2, False otherwise."""
    if edge1 == edge2:
        return False
    if not edge_intersect(v1, v2, edge2):
        return True
    edge1_dist = vertex_distance(v1, v2, edge1)
    edge2_dist = vertex_distance(v1, v2, edge2)
    if edge1_dist > edge2_dist:
        return False
    if edge1_dist < edge2_dist:
        return True
    # If the distance is equal, compare edge angles.
    if edge1_dist == edge2_dist:
        if edge1.v1 in edge2:
            same_Vertex = edge1.v1
        else:
            same_Vertex = edge1.v2
        angle_edge1 = angle2(v1, v2, edge1.get_adjacent(same_Vertex))
        angle_edge2 = angle2(v1, v2, edge2.get_adjacent(same_Vertex))
        if angle_edge1 < angle_edge2:
            return True
        return False


class EdgeSet():
    def __init__(self):
        self._open_edges = []

    def insert(self, v1, v2, edge):
        self._open_edges.insert(self._index(v1, v2, edge), edge)

    def delete(self, v1, v2, edge):
        index = self._index(v1, v2, edge) - 1
        if self._open_edges[index] == edge:
            del self._open_edges[index]

    def smallest(self):
        return self._open_edges[0]

    def _index(self, v1, v2, edge):
        lo = 0
        hi = len(self._open_edges)
        while lo < hi:
            mid = (lo+hi)//2
            if cmp_edges(v1, v2, edge, self._open_edges[mid]):
                hi = mid
            else:
                lo = mid + 1
        return lo

    def __len__(self):
        return len(self._open_edges)

    def __getitem__(self, index):
        return self._open_edges[index]
