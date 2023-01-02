from visible_vertices import *
from shortest_path import *


class VisibilityGraph:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph  # holds original obstacle graph
        self.visibility_graph = Graph()  # holds visibility connections

    def visible_from(self, O: Vertex) -> list:
        """return list of edges that represent visibility rays (to be added into visibility graph)"""
        edges = []
        for vis in visible_vertices(O, self.graph):
            edges.append(Edge(O, vis))
        return edges

    def shortest_path(self, start: Vertex, stop: Vertex) -> list:
        """return shortest path (in sum of graph and visibility_graph) as list of edges"""
        return dijkstra(self.graph | self.visibility_graph, start, stop)

    def gen_vis_graph(self):
        verts = self.graph.get_verts()
        for vert in verts:
            for edge in self.visible_from(vert):
                self.visibility_graph.add_edge(edge)

    def union(self):
        return self.graph | self.visibility_graph
