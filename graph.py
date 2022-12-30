from collections import defaultdict


class Vertex():
    def __init__(self, x, y, polygon_id=-1):
        self.x = float(x)
        self.y = float(y)
        self.polygon_id = polygon_id

    def __eq__(self, vert):
        return vert and self.x == vert.x and self.y == vert.y

    def __str__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)

    def __repr__(self):
        return "Vertex(%.2f, %.2f)" % (self.x, self.y)

    def __hash__(self):
        return self.x.__hash__() ^ self.y.__hash__()

    def __lt__(self, vert):
        return hash(self) < hash(vert)

class Edge():
    def __init__(self, vert1, vert2):
        self.v1 = vert1
        self.v2 = vert2

    def get_adjacent(self, vert):
        if vert == self.v1:
            return self.v2
        return self.v1

    def __eq__(self, edge):
        if self.v1 == edge.v1 and self.v2 == edge.v2:
            return True
        if self.v1 == edge.v2 and self.v2 == edge.v1:
            return True
        return False

    def __str__(self):
        return "({}, {})".format(self.v1, self.v2)

    def __repr__(self):
        return "Edge({!r}, {!r})".format(self.v1, self.v2)

    def __contains__(self, vert):
        return self.v1 == vert or self.v2 == vert

    def __hash__(self):
        return self.v1.__hash__() ^ self.v2.__hash__()


class Graph():
    def __init__(self, figs=None):
        self.graph = defaultdict(set)       # set of verticies
        self.edges = set()                  # set of edges
        self.polygons = defaultdict(set)    # set of polugons

        if figs is not None:
            poly_id = 0
            for fig in figs:
                lines = fig.lines
                first_vert = Vertex(lines[0][0][0], lines[0][0][1], poly_id)
                prev_vert = first_vert
                for i in range(len(lines)-1):
                    next = lines[(i + 1) % len(lines)]
                    next_vert = Vertex(next[0][0], next[0][1], poly_id)
                    edge = Edge(prev_vert, next_vert)
                    prev_vert = next_vert
                    self.add_edge(edge)
                    self.polygons[poly_id].add(edge)
                edge = Edge(prev_vert, first_vert)
                self.add_edge(edge)
                self.polygons[poly_id].add(edge)
                poly_id += 1

    def get_adjacent_verts(self, vert):
        return [edge.get_adjacent(vert) for edge in self[vert]]

    def get_verts(self):
        return list(self.graph)

    def get_edges(self):
        return self.edges

    def add_edge(self, edge):
        self.edges.add(edge)
        self.graph[edge.v1].add(edge)
        self.graph[edge.v2].add(edge)

    def add_vert(self, vert):
        if vert not in self.graph:
            self.graph[vert] = set()

    def __contains__(self, item):
        if isinstance(item, Vertex):
            return item in self.graph
        if isinstance(item, Edge):
            return item in self.edges
        return False

    def __getitem__(self, vert):
        if vert in self.graph:
            return self.graph[vert]
        return set()

    def __str__(self):
        res = ""
        for vert in self.graph:
            res += "\n" + str(vert) + ": "
            for edge in self.graph[vert]:
                res += str(edge)
        return res

    def __repr__(self):
        return self.__str__()

    def __or__(self, other):
        uni = Graph()
        for vert in self.graph.keys():
            uni.graph[vert] = self.graph[vert] | other[vert]
        for vert in other.graph.keys():
            uni.graph[vert] = self.graph[vert] | other[vert]
        uni.edges = self.edges | other.edges
        return uni
