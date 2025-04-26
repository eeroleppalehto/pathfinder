import copy

def dfs_steps(maze, start, end, snapshot_interval=1):
    original            = [row.copy() for row in maze]
    search_stack        = [(start[0], start[1], False)]  # stack for DFS (x, y, backtrack)
    visited_cells       = set()
    parent_cells        = {}
    snapshots           = [] # history of changes for visualization
    pending_snapshot    = []
    final_path          = []
    step_count          = 0
    found_path          = False
    num_rows            = len(maze)
    num_columns         = len(maze[0])
    
    END_POINTS          = ('S', 'E')
    WALL                = 1
    EMPTY               = 0

    while search_stack:
        x, y, backtrack = search_stack.pop()
        current_cell = (x, y)

        # stop when end is reached
        if current_cell == end:
            found_path = True
            break

        # unmark visited cell on backtrack (for visualization)
        if backtrack:
            if original[x][y] not in END_POINTS:
                original[x][y] = EMPTY
                step_count += 1

        else:
            if current_cell in visited_cells:
                continue

            visited_cells.add(current_cell)

            # mark the cell as visited 
            if original[x][y] not in END_POINTS:
                original[x][y] = 'V'
                pending_snapshot.append((x, y, 'V'))
                step_count += 1

            search_stack.append((x, y, True))

            # to generate neighbouring cells
            for direction_x, direction_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
                neighbour_x = x + direction_x
                neighbour_y = y + direction_y
    
                out_of_bounds = (
                    neighbour_x < 0 or neighbour_x >= num_rows 
                    or neighbour_y < 0 or neighbour_y >= num_columns
                )
                if out_of_bounds:
                    continue
                if original[neighbour_x][neighbour_y] == WALL:
                    continue
                if (neighbour_x, neighbour_y) in visited_cells:
                    continue
            
                parent_cells[(neighbour_x, neighbour_y)] = current_cell
                search_stack.append((neighbour_x, neighbour_y, False))

        # take snapshot at intervals
        if (step_count % snapshot_interval == 0 and pending_snapshot):
            snapshots.append(pending_snapshot.copy())
            pending_snapshot.clear()
            
    # append any remaining changes
    if pending_snapshot:
        snapshots.append(pending_snapshot.copy())

    # record the final shortest path
    if found_path:
        node = end
        while node != start:
            final_path.append(node)
            node = parent_cells[node]

        final_path.append(start)
        final_path.reverse()
        final_path_snapshot = [
            (x, y, 'P') 
            for x, y in final_path 
            if original[x][y] not in END_POINTS
        ]

        if final_path_snapshot:
            snapshots.append(final_path_snapshot)

    return (final_path if found_path else []), snapshots
