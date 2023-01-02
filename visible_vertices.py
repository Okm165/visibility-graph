from trig import *


def visible_vertices(vert: Vertex, graph: Graph):
    """returns list of verts in graph visible by <vert>"""
    edges = graph.get_edges()
    verts = graph.get_verts()
    verts.sort(key=lambda p: (angle(vert, p), distance(vert, p)))

    # Initialize edge_set with any intersecting edges on the half line from
    # vert along the positive x-axis
    edge_set = EdgeSet()
    vert_inf = Vertex(INF, vert.y)
    for edge in edges:
        if vert in edge:
            continue
        if edge_intersect(vert, vert_inf, edge):
            if on_segment(vert, edge.v1, vert_inf):
                continue
            if on_segment(vert, edge.v2, vert_inf):
                continue
            edge_set.insert(vert, vert_inf, edge)

    visible = []
    for p in verts:
        if p == vert:
            continue

        # Update edge_set - remove clock wise edges incident on p
        if edge_set:
            for edge in graph[p]:
                if ccw(vert, p, edge.get_adjacent(p)) == CW:
                    edge_set.delete(vert, p, edge)

        # Check if p is visible from vert
        is_visible = False
        if len(edge_set) == 0:
            is_visible = True
        elif not edge_intersect(vert, p, edge_set.smallest()):
            is_visible = True

        if is_visible and p not in graph.get_adjacent_verts(vert):
            is_visible = not edge_into_polygon(vert, p, graph)

        if is_visible:
            visible.append(p)

        # Update edge_set - Add counter clock wise edges incident on p
        for edge in graph[p]:
            if (vert not in edge) and ccw(vert, p, edge.get_adjacent(p)) == CCW:
                edge_set.insert(vert, p, edge)

    return visible
