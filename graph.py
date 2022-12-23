from collections import defaultdict


class Vertex:
    def __init__(self, x, y) -> None:
        self.x = float(x)
        self.y = float(y)

    def __mul__(self, val):
        return Vertex(self.x*val, self.y*val)

    def __eq__(self, vertex):
        return vertex and self.x == vertex.x and self.y == vertex.y

    def __ne__(self, vertex):
        return not self.__eq__(vertex)

    def __str__(self):
        return "(%.3f, %.3f)" % (self.x, self.y)

    def __repr__(self):
        return "Vertex(%.3f, %.3f)" % (self.x, self.y)

    def __hash__(self):
        return self.x.__hash__() ^ self.y.__hash__()


class Edge:
    def __init__(self, vertex1, vertex2):
        self.v1 = vertex1
        self.v2 = vertex2

    def get_adjacent(self, vert):
        if vert == self.v1:
            return self.v2
        return self.v1

    def __contains__(self, vertex):
        return self.v1 == vertex or self.v2 == vertex

    def __eq__(self, edge):
        if self.v1 == edge.v1 and self.v2 == edge.v2:
            return True
        if self.v1 == edge.v2 and self.v2 == edge.v1:
            return True
        return False

    def __ne__(self, edge):
        return not self.__eq__(edge)

    def __str__(self):
        return "({}, {})".format(self.v1, self.v2)

    def __repr__(self):
        return "Edge({!r}, {!r})".format(self.v1, self.v2)

    def __hash__(self):
        return self.v1.__hash__() ^ self.v2.__hash__()


class Graph:
    def __init__(self, figs):
        self.graph = defaultdict(set)
        self.edges = set()

        for fig in figs:
            lines = fig.lines
            first_vert = Vertex(lines[0][0][0], lines[0][0][1])
            prev_vert = first_vert
            for i in range(len(lines)-1):
                next = lines[(i + 1) % len(lines)]
                next_vert = Vertex(next[0][0], next[0][1])
                edge = Edge(prev_vert, next_vert)
                prev_vert = next_vert
                self.add_edge(edge)
            edge = Edge(prev_vert, first_vert)
            self.add_edge(edge)

    def get_adjacent_edges(self, vert):
        return list(self[vert])

    def get_adjacent_verticies(self, vert):
        return [edge.get_adjacent(vert) for edge in self[vert]]

    def get_verticies(self):
        return list(self.graph)

    def get_edges(self):
        return self.edges

    def add_edge(self, edge):
        self.graph[edge.v1].add(edge)
        self.graph[edge.v2].add(edge)
        self.edges.add(edge)

    def __str__(self):
        res = ""
        for vertex in self.graph:
            res += "\n" + str(vertex) + ": {"
            for edge in self.graph[vertex]:
                res += str(edge)
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

    def __getitem__(self, item):
        if item in self.graph:
            return self.graph[item]
        return set()
