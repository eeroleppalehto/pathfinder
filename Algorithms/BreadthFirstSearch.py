# Algorithms/BreadthFirstSearch.py
from queue import Queue
import copy

def bfs_steps(maze, start, end, snapshot_interval=1):
        original = [row.copy() for row in maze]
        steps = []
        current_changes = []
        move_count = 0
        q = Queue()
        q.put((start, []))
        visited = set()
        final_path = []
        endpoints = ('S', 'E')

        # grab the next node and the path to that node
        while not q.empty():
            (x, y), path = q.get()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if original[x][y] not in endpoints:
                current_changes.append((x, y, 'V'))
                original[x][y] = 'V'
            move_count += 1
            # periodically take a snapshot of steps
            if move_count % snapshot_interval == 0:
                if current_changes:
                    steps.append(current_changes)
                    current_changes = []
            if (x, y) == end:
                final_path = path + [(x, y)]
                break
            # add all the possible neighbouring nodes
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x+dx, y+dy
                if 0<=nx<len(original) and 0<=ny<len(original[0]) and original[nx][ny] !=1:
                    q.put(((nx, ny), path + [(x, y)]))
        # append any changes left since last snapshot
        if current_changes:
            steps.append(current_changes)
        path_changes = []
        if final_path:
            for (x,y) in final_path:
                if original[x][y] not in endpoints:
                    path_changes.append((x,y,'P'))
            steps.append(path_changes)
        return final_path, steps
