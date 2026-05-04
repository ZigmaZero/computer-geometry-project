def bbox_intersects(bbox1: tuple[float, float, float, float], bbox2: tuple[float, float, float, float]) -> bool:
    # (minx1, miny1, maxx1, maxy1), (minx2, miny2, maxx2, maxy2)
    return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
                bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])