# main.py for starting the program and managing it.

"""
System Monitor: A terminal-based tool to gather and display system resource information
including CPU, memory, disks, network, sensors, and other system details.
"""

MAIN_FILE_VERSION = "1.0.0"

from log_config import log
from tkinter import filedialog
import tkinter
import time
import json
import sys
import os

try:
    # Import system info gathering and display modules
    from gather_info import GatherSystemInfo
    from display_renderer import DisplayRenderer
except ImportError as e:
    log.error(f"{type(e).__name__}: {e}")
    sys.exit(1)

log.info("Successfully imported files.")

def main():
    # Create instances for gathering and rendering system info
    gatherer = GatherSystemInfo()
    renderer = DisplayRenderer()

    log.info("System Monitor Started.")

    try:
        while True:
            # Gather and display system info
            info = gatherer.system_info()
            renderer.render_system_info(info)

            # Prompt user for update or save
            if input("Press enter to update.\nEnter 's' to save: ").lower() == "s":
                print("=" * 50)
                save(info)
                input("Press enter to continue...")
                time.sleep(3)

    except KeyboardInterrupt:
        # Handle user interruption gracefully
        log.info("System monitor stopped by user (Ctrl+C).")
        print("\n--- System Monitor Stopped ---")
    except Exception as e:
        # Log any unexpected errors and exit
        log.critical(f"An unexpected error occurred: {type(e).__name__}: {e}")
        sys.exit(1)
        
def save(info):
    log.debug("Attempting to save as JSON")

    filename = "system-info"
    filetype = ".json"
    filename = input("Enter your file name: ")
    filename += filetype
    
    while True:
        try:

            # Use Tkinter to open a directory selection dialog
            root = tkinter.Tk()
            root.withdraw()
            directory = filedialog.askdirectory(title="Select a directory to save the info JSON file")
            root.destroy()

            if not directory:  # User cancelled the dialog
                print("Directory selection cancelled. Aborting save.")
                log.info("Directory selection cancelled. Aborting save.")
                return

            if os.path.isdir(directory):

                path = os.path.join(directory, filename)
                write_file(info, path)

                log.info(f"Successfully created {filename}")
                print(f"{filename} was created at: {path}")
                input("Press enter to exit...")
                sys.exit()

            else:
                print("ERROR: Invalid path!")
                retry = input("Invalid path! Retry? (y/n): ").strip().lower()

                if retry == "y":
                    continue
                else:
                    return

        except PermissionError as e:
            log.warning(f"Exception: {type(e).__name__}: {e}")
            print("Exception: Permission denied for the selected path.")
            retry = input("Permission error! Retry? (y/n): ").strip().lower()

            if retry == "y":
                log.warning("Attempting alternative path.")
                continue
            else:
                return

def write_file(info, path):
    with open(path, "w") as f:
        json.dump(info, f, indent=4)

if __name__ == "__main__":
    main()