from trig import *
from graph import *

CCW = 1
CW = -1


def visible_vertices(O: Vertex, graph: Graph) -> list:
    """ Takes vertex O and graph returns list of vertecies that are visible from O 
        complexity: O(nlogn)
    """
    visible_verts = []
    verts = graph.get_verticies()
    edges = graph.get_edges()
    verts = sort_by_angle_distance(O, verts)[1:]
    if len(verts) == 0:
        return visible_verts

    # Initialize edge_set with any intersecting edges with p
    edge_set = EdgeSet()

    p = Edge(O, verts[0])
    inf_p = Edge(O, (unit_vector(O, verts[0])*INFINITY))

    for edge in edges:
        if O in edge:
            continue
        if edge_intersect(inf_p, edge):
            # if on_segment(inf_p.v1, edge.v1, inf_p.v2):
            #     continue
            # if on_segment(inf_p.v1, edge.v2, inf_p.v2):
            #     continue
            edge_set.insert(inf_p, edge)

    # special first vert
    if len(edge_set) > 0:
        if not (edge_intersect(p, edge_set.smallest()) and edge_set.smallest() not in graph[verts[0]]):
            visible_verts.append(verts[0])

    for vert in verts[1:]:
        if vert == O:
            continue
        p.v2 = vert
        inf_p.v2 = unit_vector(O, vert)*INFINITY
        # Update edge_set - remove counter clock wise edges incident on vert
        if len(edge_set) > 0:
            for edge in graph[vert]:
                if ccw(O, vert, edge.get_adjacent(vert)) == CCW:
                    print("del", edge)
                    edge_set.delete(inf_p, edge)
        # VISIBLE
        visible = False
        if len(edge_set) == 0:
            visible = True
        elif not edge_intersect(p, edge_set.smallest()):
            visible = True
        
        print("set", edge_set)
        print(visible)

        if visible and vert not in graph.get_adjacent_verticies(O):
            in_polygon = edge_in_polygon(O, vert, graph)
            print(in_polygon)
            visible = not in_polygon
        print(visible)

        if visible:
            visible_verts.append(vert)

        # Update edge_set - Add clock wise edges incident on vert
        for edge in graph[vert]:
            if (O not in edge) and ccw(O, vert, edge.get_adjacent(vert)) == CW:
                print("add", edge)
                edge_set.insert(inf_p, edge)
        
        print("set", edge_set)

    return visible_verts
