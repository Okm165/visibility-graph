class Vertex:
    def __init__(self, x, y) -> None:
        self.x = float(x)
        self.y = float(y)
        self.neighbours = set()

    def add(self, vertex):
        self.neighbours.add(vertex)

    def remove(self, vertex):
        self.neighbours.remove(vertex)

    def clear(self):
        self.neighbours.clear()

    def __eq__(self, vertex):
        return vertex and self.x == vertex.x and self.y == vertex.y

    def __ne__(self, vertex):
        return not self.__eq__(vertex)

    def __str__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)

    def __repr__(self):
        return "Vertex(%.2f, %.2f)" % (self.x, self.y)

    def __hash__(self):
        return self.x.__hash__() ^ self.y.__hash__()


class Edge():
    def __init__(self, vertex1, vertex2):
        self.v1 = vertex1
        self.v2 = vertex2
        # make them neighbours
        self.v1.neighbours.add(self.v2)
        self.v2.neighbours.add(self.v1)

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
    def __init__(self):
        self.graph = set()
        self.edges = set()

    def get_vertices(self):
        return list(self.graph)

    def get_edges(self):
        return list(self.edges)

    def add_edge(self, edge):
        self.graph.add(edge.v1)
        self.graph.add(edge.v2)
        self.edges.add(edge)

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
