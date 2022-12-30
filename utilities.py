from graph import *
from geometria import *

def edges_to_linesCollection(edges: list, color = "blue") -> LinesCollection:
    return LinesCollection([[(edge.v1.x, edge.v1.y), (edge.v2.x, edge.v2.y)] for edge in edges], color=color)

def graph_to_linesCollection(graph: Graph, color = "blue") -> LinesCollection:
    return edges_to_linesCollection(graph.get_edges(), color)

def vertecies_to_pointsCollection(verts: list, color = "blue") -> PointsCollection:
    return PointsCollection([(v.x, v.y) for v in verts], color=color)