# Test.py
import tkinter as tk
from UserInterface.UserInterface import UserInterface
from MazeGenerator import MazeGenerator
from MazeSolver import MazeSolver

def solver_factory(algorithm_name):
    return MazeSolver(algorithm=algorithm_name)

def main():
    root = tk.Tk()
    generator = MazeGenerator()
    app = UserInterface(root, generator, solver_factory)
    root.mainloop()

if __name__ == "__main__":
    main()
