from queue import PriorityQueue
import copy

def dijkstra_steps(maze, start, end, snapshot_interval=1):
    original            = [row.copy() for row in maze]
    priority_queue      = PriorityQueue()
    # enqueue (cost, x, y, path_so_far)
    priority_queue.put((0, start[0], start[1], []))
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

    while not priority_queue.empty():
        cost, x, y, path = priority_queue.get()
        current_cell     = (x, y)

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
            final_path = path + [(x, y)]
            break

        # explore neighbours
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

            priority_queue.put((cost + 1, neighbour_x, neighbour_y, path + [(x, y)]))

    # any remaining visited‐cell snapshots
    if pending_snapshot:
        snapshots.append(pending_snapshot.copy())

    # record the final shortest path
    if found_path:
        final_path_snapshot = [
            (x, y, 'P')
            for x, y in final_path
            if original[x][y] not in END_POINTS
        ]
        if final_path_snapshot:
            snapshots.append(final_path_snapshot)

    return (final_path if found_path else []), snapshots
