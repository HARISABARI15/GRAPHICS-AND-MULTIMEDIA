def inside(p, edge):
    x, y = p
    (x1, y1), (x2, y2) = edge
    return (x2 - x1) * (y - y1) >= (y2 - y1) * (x - x1)

def intersection(p1, p2, edge):
    x1, y1 = p1
    x2, y2 = p2
    (ex1, ey1), (ex2, ey2) = edge
    dx, dy = x2 - x1, y2 - y1
    edge_dx, edge_dy = ex2 - ex1, ey2 - ey1
    denominator = dx * edge_dy - dy * edge_dx
    if denominator == 0:
        return p2  # Parallel lines
    t = ((ex1 - x1) * edge_dy - (ey1 - y1) * edge_dx) / denominator
    return (x1 + t * dx, y1 + t * dy)

def sutherland_hodgman_clip(polygon, clip_edges):
    output = polygon
    for edge in clip_edges:
        input_list = output
        output = []
        if not input_list:
            break
        s = input_list[-1]
        for e in input_list:
            if inside(e, edge):
                if not inside(s, edge):
                    output.append(intersection(s, e, edge))
                output.append(e)
            elif inside(s, edge):
                output.append(intersection(s, e, edge))
            s = e
    return output

# Example usage:
polygon = [(50,150), (200,50), (350,150), (350,300), (250,300), (200,250), (150,350), (100,250), (100,200)]
clip_rect = [(100,100), (300,100), (300,300), (100,300)]
clip_edges = [ (clip_rect[i], clip_rect[(i+1)%4]) for i in range(4) ]

clipped_polygon = sutherland_hodgman_clip(polygon, clip_edges)
print("Clipped Polygon:", clipped_polygon)