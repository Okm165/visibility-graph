from queue import PriorityQueue
from trig import distance
from graph import *


def dijkstra(graph: Graph, start: Vertex, stop: Vertex) -> list:
    """ Returns shortest path in graph between start and end as list of edges """
    distances = {vertex: float('inf') for vertex in graph.get_verticies()}
    visited = {vertex: False for vertex in graph.get_verticies()}
    parents = {vertex: None for vertex in graph.get_verticies()}

    Q = PriorityQueue()
    distances[start] = 0
    visited[start] = True
    Q.put((distances[start], start))

    while not Q.empty():
        dist, vert = Q.get()
        for neigh_vert in graph.get_adjacent_verticies(vert):
            if visited[neigh_vert] == True:
                continue
            new_dist = dist + distance(vert, neigh_vert)
            if new_dist < distances[neigh_vert]:
                distances[neigh_vert] = new_dist
                parents[neigh_vert] = vert
                Q.put((new_dist, neigh_vert))
        visited[vert] = True

    # reconstruct shortest path
    path = []
    curr = stop
    if curr is None:
        return path
    while parents[curr] is not None:
        path.append(Edge(curr, parents[curr]))
        curr = parents[curr]
    return path
