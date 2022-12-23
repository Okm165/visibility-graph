from graph import Graph
from vertex_edge import Edge, Vertex

v1 = Vertex(1, 0, 0)
v2 = Vertex(2, 0, 1)
v3 = Vertex(3, 1, 1)
v4 = Vertex(4, 1, 0)
v5 = Vertex(5, 1, 2)
v6 = Vertex(6, 2, 2)
v7 = Vertex(7, 2, 1)
v8 = Vertex(8, 2, 0)

# Create a graph and add the vertices
g = Graph([])
g.add_edge(Edge(v1, v2))
g.add_edge(Edge(v2, v3))
g.add_edge(Edge(v3, v4))
g.add_edge(Edge(v4, v1))
g.add_edge(Edge(v3, v5))
g.add_edge(Edge(v5, v6))
g.add_edge(Edge(v6, v7))
g.add_edge(Edge(v7, v8))
g.add_edge(Edge(v8, v4))
g.add_edge(Edge(v3, v6))

print(g.dijkstra(v1,v6))