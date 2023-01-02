from visible_vertices import *
from shortest_path import *
from utilities import *


class VisibilityGraph:
    def __init__(self, graph: Graph, redlines, start, end) -> None:
        self.graph = graph  # holds original obstacle graph
        self.visibility_graph = Graph()  # holds visibility connections
        self.redlines = redlines
        self.scenes = []
        self.start = start
        self.end = end

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
        "appends all visible verticies from the vert and add scene"
        self.scenes.append(Scene(
                points = 
                [PointsCollection([(self.start.x, self.start.y), (self.end.x, self.end.y)], color = "green")], 
                lines = 
                [self.redlines] ))
        verts = self.graph.get_verts()
        for vert in verts:
            for edge in self.visible_from(vert):
                self.visibility_graph.add_edge(edge)
            self.scenes.append(Scene(
                points = 
                [PointsCollection([(self.start.x, self.start.y), (self.end.x, self.end.y)], color = "green"),
                PointsCollection([(vert.x, vert.y)], color = "purple")], 
                lines = 
                [graph_to_linesCollection(self.union(), "grey"), self.redlines] ))

    def union(self):
        return self.graph | self.visibility_graph

    def shortest_path_scene(self):
        """add shortest path to visualization"""
        self.scenes.append(Scene(
            points = [PointsCollection([(self.start.x, self.start.y), (self.end.x, self.end.y)],
            color = "green")] , 
            lines = [graph_to_linesCollection(self.union(), "grey"), 
            self.redlines, 
            edges_to_linesCollection(self.shortest_path(self.start, self.end), "green")]))
