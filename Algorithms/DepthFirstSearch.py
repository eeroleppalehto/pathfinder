import copy

def dfs_steps(maze, start, end, snapshot_interval=1):
    original = [row.copy() for row in maze]
    steps = []
    current_changes = []
    move_count = 0
    visited = set()
    stack = []
    found = False
    path = []
    final_path = []

    # Initialize stack with start position and backtracking flag
    stack.append((start[0], start[1], False))

    while stack:
        x, y, is_backtracking = stack.pop()

        if (x, y) == end:
            found = True
            path.append((x, y))
            continue

        if not is_backtracking:
            # First visit to this node
            if (x, y) not in visited:
                visited.add((x, y))
                if original[x][y] not in ('S', 'E'):
                    current_changes.append((x, y, 'V'))
                    original[x][y] = 'V'
                    move_count += 1
                # Push the backtracking phase
                stack.append((x, y, True))
                # Explore neighbors in reverse order to maintain original direction order (up, down, left, right)
                for dx, dy in reversed([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(original) and 0 <= ny < len(original[0]):
                        if original[nx][ny] != 1 and (nx, ny) not in visited:
                            stack.append((nx, ny, False))
        else:
            # Backtracking phase
            if found:
                path.append((x, y))
            else:
                if original[x][y] not in ('S', 'E'):
                    current_changes.append((x, y, 0))
                    original[x][y] = 0
                    move_count += 1

        # Capture snapshot if needed
        if move_count % snapshot_interval == 0 and current_changes:
            steps.append(current_changes.copy())
            current_changes.clear()

    # Handle remaining changes
    if current_changes:
        steps.append(current_changes.copy())
        current_changes.clear()

    # If path is found, mark the final path
    if found:
        # The path is collected in reverse order (from end to start)
        final_path = list(reversed(path))
        # Add the path changes to steps
        path_changes = []
        for (x, y) in final_path:
            if original[x][y] not in ('S', 'E'):
                path_changes.append((x, y, 'P'))
        if path_changes:
            steps.append(path_changes)
    else:
        final_path = []

    return final_path, steps