from collections import defaultdict
from heapq import heappop, heappush
from trig import distance
from vertex_edge import Vertex, Edge


class Graph:
    def __init__(self, figs):
        self.graph = defaultdict(set)
        self.edges = set()

        vert_cnt = 0
        for fig in figs:
            lines = fig.lines
            first_vert = Vertex(vert_cnt, lines[0][0][0], lines[0][0][1])
            prev_vert = first_vert
            vert_cnt += 1
            for i in range(len(lines)-1):
                next = lines[(i + 1) % len(lines)]
                next_vert = Vertex(vert_cnt, next[0][0], next[0][1])
                edge = Edge(prev_vert, next_vert)
                prev_vert = next_vert
                self.add_edge(edge)
                vert_cnt += 1
            edge = Edge(prev_vert, first_vert)
            self.add_edge(edge)

    def get_adjacent_edges(self, vert):
        return list(self.graph[vert])

    def get_verticies(self):
        return list(self.graph)

    def get_edges(self):
        return self.edges

    def add_edge(self, edge):
        self.graph[edge.v1].add(edge)
        self.graph[edge.v2].add(edge)
        self.edges.add(edge)

        ''' backward edge - do we want it?'''
        # self.edges.add(Edge(edge.v2, edge.v1))

    def __str__(self):
        res = ""
        for vertex in self.graph:
            res += "\n" + str(vertex) + ": {"
            for neighbour in vertex.neighbours:
                res += str(neighbour)
            res += "}"
        return res

    def __repr__(self):
        return self.__str__()

    def __contains__(self, item):
        if isinstance(item, Vertex):
            return item in self.graph
        if isinstance(item, Edge):
            return item in self.edges
        return False

    def dijkstra(self, start, end):
        distances = {vertex: float('inf') for vertex in self.get_verticies()}
        distances[start] = 0
        previous_vertices = {vertex: None for vertex in self.get_verticies()}
        heap = [(0, start)]
        while heap:
            curr_distance, current_vertex = heappop(heap)
            for edge in self.get_adjacent_edges(current_vertex):
                if edge.v1 == current_vertex:
                    next_vertex = edge.v2
                else:
                    next_vertex = edge.v1
                next_distance = curr_distance + distance(current_vertex, next_vertex)
                if next_distance < distances[next_vertex]:
                    distances[next_vertex] = next_distance
                    previous_vertices[next_vertex] = current_vertex
                    heappush(heap, (next_distance, next_vertex))

        # shortest_path = []
        # current_vertex = end
        # while current_vertex is not None:
        #     shortest_path.append(current_vertex)
        #     current_vertex = previous_vertices[current_vertex]

        return distances[end]
