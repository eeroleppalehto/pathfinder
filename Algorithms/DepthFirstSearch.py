import copy

def dfs_steps(maze, start, end, snapshot_interval=1):
    rows, cols = len(maze), len(maze[0])
    original = [r.copy() for r in maze]
    visited = set()
    parent = {}
    stack = [(start[0], start[1], False)]
    steps, changes = [], []
    count, found = 0, False
    endpoints = ('S', 'E')

    while stack:
        x, y, back = stack.pop()
        if (x, y) == end:
            found = True
            break

        if back:
            if original[x][y] not in endpoints:
                original[x][y] = 0
                count += 1
        else:
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if original[x][y] not in endpoints:
                changes.append((x, y, 'V'))
                original[x][y] = 'V'
                count += 1
            stack.append((x, y, True))
            # to generate neighbouring cells
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
                nx, ny = x + dx, y + dy
                # check if node has not been visited
                if 0 <= nx < rows and 0 <= ny < cols and original[nx][ny] != 1 and (nx, ny) not in visited:
                    # keep track where we came from
                    parent[(nx, ny)] = (x, y)
                    stack.append((nx, ny, False))
        # periodically take a snapshot of steps
        if count % snapshot_interval == 0 and changes:
            steps.append(changes.copy())
            changes.clear()
            
    # append any changes left since last snapshot
    if changes:
        steps.append(changes.copy())

    path = []
    if found:
        node = end
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()
        pchg = [(x, y, 'P') for x, y in path if original[x][y] not in endpoints]
        if pchg:
            steps.append(pchg)

    return (path if found else []), steps
