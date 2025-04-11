def heuristic(a, b):
    """Manhattan Distance heuristic for A*"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
