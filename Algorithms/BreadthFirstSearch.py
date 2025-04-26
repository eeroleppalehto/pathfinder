    # Algorithms/BreadthFirstSearch.py
from queue import Queue
import copy

def bfs_steps(maze, start, end, snapshot_interval=1):
    original            = [row.copy() for row in maze]
    search_queue        = Queue()
    search_queue.put((start[0], start[1], []))
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

    while not search_queue.empty():
        x, y, path     = search_queue.get()
        current_cell   = (x, y)

        if current_cell in visited_cells:
            continue
        visited_cells.add(current_cell)

        # mark the cell as visited and add to snapshot
        if original[x][y] not in END_POINTS:
            original[x][y]      = 'V'
            pending_snapshot.append((x, y, 'V'))
            step_count          += 1

        # take snapshot at intervals
        if step_count % snapshot_interval == 0 and pending_snapshot:
            snapshots.append(pending_snapshot.copy())
            pending_snapshot.clear()

        # check for end point
        if current_cell == end:
            found_path = True
            final_path = path + [(x, y)]
            break

        # enqueue neighboring cells
        for direction_x, direction_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_x = x + direction_x
            neighbor_y = y + direction_y

            is_out_of_bounds = (
                neighbor_x < 0 or neighbor_x >= num_rows or
                neighbor_y < 0 or neighbor_y >= num_columns
            )
            if is_out_of_bounds:
                continue
            if original[neighbor_x][neighbor_y] == WALL:
                continue
            if (neighbor_x, neighbor_y) in visited_cells:
                continue

            search_queue.put((neighbor_x, neighbor_y, path + [(x, y)]))

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