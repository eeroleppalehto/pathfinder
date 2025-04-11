# Algorithms.py
import copy
from queue import Queue, PriorityQueue
import heapq

def bfs_steps(maze, start, end):
    """Breadth-First Search that records intermediate steps.
    Visited cells are marked with 'V'. BFS does not backtrack, so only forward exploration is shown.
    Returns: (final_path, steps)
    """
    steps = []
    rows, cols = len(maze), len(maze[0])
    q = Queue()
    q.put((start, []))
    visited = set()
    
    # Record the initial state.
    steps.append(copy.deepcopy(maze))
    
    while not q.empty():
        (x, y), path = q.get()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if maze[x][y] not in ('S', 'E'):
            maze[x][y] = 'V'
        steps.append(copy.deepcopy(maze))
        if (x, y) == end:
            return path + [(x, y)], steps
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1:
                q.put(((nx, ny), path + [(x, y)]))
    return [], steps

def dfs_steps(maze, start, end):
    """Depth-First Search that records intermediate steps and shows backtracking.
    'V' marks cells as visited; when backtracking, the cell is reset to 0.
    Returns: (final_path, steps)
    """
    steps = []
    rows, cols = len(maze), len(maze[0])
    visited = set()
    path = []
    found = False

    # Record initial state.
    steps.append(copy.deepcopy(maze))

    def dfs(x, y):
        nonlocal found
        if found:
            return True
        visited.add((x, y))
        path.append((x, y))
        if maze[x][y] not in ('S', 'E'):
            maze[x][y] = 'V'
        steps.append(copy.deepcopy(maze))
        if (x, y) == end:
            found = True
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx][ny] != 1:
                if dfs(nx, ny):
                    return True
        # Backtracking step:
        path.pop()
        if maze[x][y] not in ('S', 'E'):
            maze[x][y] = 0  # Reset the cell (backtrack)
        steps.append(copy.deepcopy(maze))
        return False

    dfs(start[0], start[1])
    return (path if found else []), steps

def dijkstra_steps(maze, start, end):
    """Dijkstra's Algorithm that records exploration steps.
    Each visited cell is marked with 'V'. Does not show backtracking.
    Returns: (final_path, steps)
    """
    steps = []
    rows, cols = len(maze), len(maze[0])
    pq = PriorityQueue()
    pq.put((0, start, []))
    visited = set()
    
    steps.append(copy.deepcopy(maze))
    
    while not pq.empty():
        cost, (x, y), path = pq.get()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if maze[x][y] not in ('S', 'E'):
            maze[x][y] = 'V'
        steps.append(copy.deepcopy(maze))
        if (x, y) == end:
            return path + [(x, y)], steps
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1:
                pq.put((cost + 1, (nx, ny), path + [(x, y)]))
    return [], steps

def heuristic(a, b):
    """Manhattan Distance heuristic for A*"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_steps(maze, start, end):
    """A* Algorithm that records exploration steps.
    Visited cells are marked with 'V'. Does not show backtracking.
    Returns: (final_path, steps)
    """
    steps = []
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start, []))
    visited = set()

    steps.append(copy.deepcopy(maze))
    
    while open_set:
        _, (x, y), path = heapq.heappop(open_set)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if maze[x][y] not in ('S', 'E'):
            maze[x][y] = 'V'
        steps.append(copy.deepcopy(maze))
        if (x, y) == end:
            return path + [(x, y)], steps
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1:
                g_cost = len(path) + 1
                f_cost = g_cost + heuristic((nx, ny), end)
                heapq.heappush(open_set, (f_cost, (nx, ny), path + [(x, y)]))
    return [], steps
