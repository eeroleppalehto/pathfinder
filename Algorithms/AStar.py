import heapq
import copy

# change to adjust how greedy A* will be
HEURISTIC_WEIGHT = 2.0


# Manhattan distance heuristic for grid
def heuristic(a, b):
     return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_steps(maze, start, end, snapshot_interval=1):
    original            = [row.copy() for row in maze]
    priority_queue      = []
    heapq.heappush(
        priority_queue,
        (0, start[0], start[1], [])
    )
    
    visited_cells       = set()
    snapshots           = []
    pending_snapshot    = []
    step_count          = 0
    found_path          = False
    final_path          = []
    num_rows            = len(maze)
    num_columns         = len(maze[0])

    END_POINTS          = ('S', 'E')
    WALL                = 1
    EMPTY               = 0

    while priority_queue:
        f_cost, x, y, path = heapq.heappop(priority_queue)
        current_cell       = (x, y)

        if current_cell in visited_cells:
            continue
        visited_cells.add(current_cell)

        # mark as visited
        if original[x][y] not in END_POINTS:
            original[x][y] = 'V'
            pending_snapshot.append((x, y, 'V'))
        step_count += 1

        # take snapshot at intervals
        if step_count % snapshot_interval == 0 and pending_snapshot:
            snapshots.append(pending_snapshot.copy())
            pending_snapshot.clear()

        # reached the end
        if current_cell == end:
            found_path = True
            final_path  = path + [(x, y)]
            break

        # explore neighbors
        for direction_x, direction_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbour_x = x + direction_x
            neighbour_y = y + direction_y

            out_of_bounds = (
                neighbour_x < 0 or neighbour_x >= num_rows or
                neighbour_y < 0 or neighbour_y >= num_columns
            )
            if out_of_bounds:
                continue
            if original[neighbour_x][neighbour_y] == WALL:
                continue
            if (neighbour_x, neighbour_y) in visited_cells:
                continue

            g_cost = len(path) + 1
            h_cost = heuristic((neighbour_x, neighbour_y), end)
            f_cost = g_cost + h_cost * HEURISTIC_WEIGHT

            heapq.heappush(
                priority_queue,
                (f_cost, neighbour_x, neighbour_y, path + [(x, y)])
            )

    # append remaining snapshots
    if pending_snapshot:
        snapshots.append(pending_snapshot.copy())

    # record the final path
    if found_path:
        final_path_snapshot = [
            (x, y, 'P')
            for x, y in final_path
            if original[x][y] not in END_POINTS
        ]
        if final_path_snapshot:
            snapshots.append(final_path_snapshot)

    return (final_path if found_path else []), snapshots
