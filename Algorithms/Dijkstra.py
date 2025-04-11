# Algorithms/Dijkstra.py
from queue import PriorityQueue
import copy
def dijkstra_steps(maze, start, end, snapshot_interval=1):
    original = [row.copy() for row in maze]
    steps = []
    current_changes = []
    move_count = 0
    pq = PriorityQueue()
    pq.put((0, start, []))
    visited = set()
    final_path = []

    while not pq.empty():
        cost, (x,y), path = pq.get()
        if (x,y) in visited:
            continue
        visited.add((x,y))
        if original[x][y] not in ('S','E'):
            current_changes.append((x,y,'V'))
            original[x][y] = 'V'
        move_count +=1
        if move_count % snapshot_interval ==0:
            if current_changes:
                steps.append(current_changes)
                current_changes = []
        if (x,y) == end:
            final_path = path + [(x,y)]
            break
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<len(original) and 0<=ny<len(original[0]) and original[nx][ny] !=1:
                pq.put((cost+1, (nx, ny), path + [(x,y)]))
    if current_changes:
        steps.append(current_changes)
    path_changes = []
    if final_path:
        for (x,y) in final_path:
            if original[x][y] not in ('S','E'):
                path_changes.append((x,y,'P'))
        steps.append(path_changes)
    return final_path, steps