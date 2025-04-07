import sys
import subprocess
import time
import os

WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
VS_CODE_INSTRUCTIONS_TEMPLATE = \
"""If VSCode does not recognize the libraries, please follow these steps:

1. Ensure your workspace is set to Trusted.
   - If you haven't been prompted to trust your workspace, do the following:
     - Open the Command Palette (Ctrl+Shift+P on Windows/Linux, Cmd+Shift+P on macOS).
     - Type 'Workspace: Manage Workspace Trust' and select it.
     - Click the option to trust your workspace.

2. Open the Command Palette in VSCode (Ctrl+Shift+P on Windows/Linux, Cmd+Shift+P on macOS).

3. Type 'Python: Select Interpreter' and select 'Python {version}'.
   - If this version does not exist, add the interpreter manually:
     - Click 'Enter interpreter path' and select: {interpreter}

4. Restart VSCode if necessary.

If you are still having issues, you may need to install the following dependencies:
"""

DEPENDENCIES = ['Pillow']  



def install_dependency(dependency):
    try:
        # Suppress pip output
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', dependency],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print(f" -> {dependency} installed successfully")
    except subprocess.CalledProcessError as error:
        print(f" -> Error installing {dependency}: {error}")

def check_and_install():
    for index, dependency in enumerate(DEPENDENCIES, start=1):
        print("===========================")
        print(f"{index}. Installing {dependency}:")
        try:
            __import__(dependency)
            print(f" -> {dependency} is already installed")
        except ImportError:
            install_dependency(dependency)
        print(f"===========================")

def save_vscode_instructions():
    version = sys.version.split()[0]
    interpreter = sys.executable

    instructions = VS_CODE_INSTRUCTIONS_TEMPLATE.format(version=version, interpreter=interpreter)
    instructions += "\n  " + "\n  ".join(DEPENDENCIES) + "\n"
    file_path = os.path.join(WORKING_DIRECTORY, "vscode_instructions.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(instructions)

    print(f"\nVSCode instructions for using the required libraries have been saved to:\n  {file_path}\n")

def wait_for_keypress():
    print("Setup complete.\n")
    print("=============================================")
    print("        Press any key to close...")
    print("=============================================")
    if sys.platform.startswith("win"):
        try:
            import msvcrt
            while True:
                if msvcrt.kbhit():
                    msvcrt.getch()
                    break
                time.sleep(0.1)
        except Exception as e:
            print(f"\nKeypress detection failed on Windows: {e}")
            input("\nPress Enter to close...")
    else:
        try:
            import tty, termios, select
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while True:
                    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if rlist:
                        sys.stdin.read(1)
                        break
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception as e:
            print(f"\nKeypress detection failed on Unix: {e}")
            input("\nPress Enter to close...")

if __name__ == '__main__':
    print("=============================================")
    print("           install_requirements.py           ")
    print("=============================================\n")
    check_and_install()
    save_vscode_instructions()
    wait_for_keypress()
