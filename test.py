from UserInterface.UserInterface import UserInterface 

import tkinter as tk
import traceback
import time
import sys

def main():
    root = tk.Tk()
    app = UserInterface(root)  # ✅ Now this correctly refers to the class
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("An error occurred. Restarting the application...")
        traceback.print_exc()
        time.sleep(1)
