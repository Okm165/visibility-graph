from trig import *
from graph import *

def visible_vertices(O: Vertex, graph: Graph):
    """ Takes vertex O and graph returns modified graph with added edges to vertecies that are visible from O """
    verts = sort_by_angle_distance(O, graph.get_vertices())
