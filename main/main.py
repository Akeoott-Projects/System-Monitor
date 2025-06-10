# main.py for starting the program and managing it.

"""
System Monitor: A terminal-based tool to gather and display system resource information
including CPU, memory, disks, network, sensors, and other system details.
"""

MAIN_FILE_VERSION = "1.0.0"

from log_config import log
import time
import sys

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
            
            # Prompt user for update or save (save not implemented)
            if input("Press enter to update.\nEnter 's' to save: ").lower() == "s":
                # Placeholder for save functionality
                print("Save functionality not implemented.")

    except KeyboardInterrupt:
        # Handle user interruption gracefully
        log.info("System monitor stopped by user (Ctrl+C).")
        print("\n--- System Monitor Stopped ---")
    except Exception as e:
        # Log any unexpected errors and exit
        log.critical(f"An unexpected error occurred: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()