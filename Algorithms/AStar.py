import heapq
import copy

HEURISTIC_WEIGHT = 2.0  # Increase to make A* greedier (1.0 = standard, 0.0 = Dijkstra)

def heuristic(a, b):
    """Manhattan Distance heuristic for A*"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_steps(maze, start, end, snapshot_interval=1):
    original = [row.copy() for row in maze]
    steps = []
    current_changes = []
    move_count = 0
    open_set = []
    heapq.heappush(open_set, (0, start, []))
    visited = set()
    final_path = []

    while open_set:
        _, (x, y), path = heapq.heappop(open_set)
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if original[x][y] not in ('S', 'E'):
            current_changes.append((x, y, 'V'))
            original[x][y] = 'V'

        move_count += 1
        if move_count % snapshot_interval == 0 and current_changes:
            steps.append(current_changes)
            current_changes = []

        if (x, y) == end:
            final_path = path + [(x, y)]
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(original) and 0 <= ny < len(original[0]) and original[nx][ny] != 1:
                g = len(path) + 1
                h = heuristic((nx, ny), end)
                f = g + h * HEURISTIC_WEIGHT
                heapq.heappush(open_set, (f, (nx, ny), path + [(x, y)]))

    if current_changes:
        steps.append(current_changes)

    path_changes = []
    if final_path:
        for (x, y) in final_path:
            if original[x][y] not in ('S', 'E'):
                path_changes.append((x, y, 'P'))
        steps.append(path_changes)

    return final_path, steps
