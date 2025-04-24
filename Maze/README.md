# Maze

This folder contains all the modules and files related to storing and manipulating the maze data. The maze is represented as a 2D array, where each cell can be either a wall or a path. The maze is generated using a recursive backtracking algorithm, which ensures that there is always a path from the start to the end of the maze.

The maze is represented as a 2D array, where each cell can be either a wall (1) or a path (0). The start and end points of the maze are represented by 'S' and 'E', respectively. When the pathfinding is visualized, the visited cells are represented by 'V', and once path is found, the path is represented by 'P'.

Example of the maze:
```Python
[
    ['S', 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 'E'],
]
```

## Contents

* `MazeApp.py`: The main application file that runs the maze generation and visualization.
* `MazeDrawing.py`: Contains the logic for drawing the maze on the screen using Pygame.
* `MazeGenerator.py`: Contains the logic for generating the maze using recursive backtracking.
* `MazeModel.py`: Contains the data structure for the maze, including the methods for showing the pathfinding process.
* `MazeRenderer.py`: Contains the logic for rendering the maze on the screen using Pygame.
* `MazeSolver.py`: Contains the logic for solving the maze using either DFS, BFS, Dijkstra, or A* algorithms.

## MazeApp.py

This file contains the main application logic for the application. It initializes the Pygame window, handles user input, and manages the maze generation and solving process. The main loop of the application is located here, which updates the display and handles events.

## MazeDrawing.py

The MazeDrawing module contains the logic for drawing on the screen. The MazeApp module serves the events to this module, which then draws the chosen tile on the screen.

## MazeGenerator.py

The MazeGenerator is responsible for generating the maze data structure. It uses a recursive backtracking algorithm to create a random maze. The maze is represented as a 2D array, where each cell can be either a wall or a path. The generator ensures that there is always a path from the start to the end of the maze. Depending on the chosen mode, the generator can also create an empty maze.

## MazeModel.py

This module is responsible for storing the maze data structure. It also contains methods for running the pathfinding algorithms and handling the pathfinding process.

## MazeRenderer.py

The MazeRenderer module is responsible for rendering the maze on the screen. It uses Pygame to draw the maze.       

## MazeSolver.py

This module contains the logic for solving the maze based on the chosen algorithm. It implements the following algorithms:
* Depth-First Search (DFS)
* Breadth-First Search (BFS)
* Dijkstra's Algorithm
* A* Algorithm
