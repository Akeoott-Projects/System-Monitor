# System-Monitor

System-Monitor is a terminal-based Python application for monitoring and displaying real-time system resource information. It provides a clear, organized view of your system's CPU, memory, disk, network, and other details, making it easy to keep track of your computer's health and performance.

## Features

- **CPU Monitoring:**  
  Displays logical CPU count, usage percentage, times (in seconds and percent), stats, and frequency.

- **Memory Monitoring:**  
  Shows virtual and swap memory statistics, including total, used, free, and percentage used.

- **Disk Monitoring:**  
  Lists all physical disk partitions with device name, mount point, filesystem type, total/used/free space, and usage percentage.

- **Network Monitoring:**  
  Reports per-interface statistics such as status (up/down), speed, bytes sent/received, and error counts.

- **Sensor Information:**  
  (Limited) Displays a note about sensor support; temperature and battery info are placeholders for future expansion.

- **Other System Info:**  
  Shows OS name/version, boot time, and currently logged-in users.

- **User-Friendly Output:**  
  Uses tables and clear formatting for easy reading in the terminal.

- **Logging:**  
  Logs important events and errors for troubleshooting.

## Requirements

  - Python 3.7+
  - [psutil](https://pypi.org/project/psutil/)
  - [tabulate](https://pypi.org/project/tabulate/)

Install dependencies with:

  ```bash
  pip install psutil tabulate
  ```

## Usage

1. **Clone or Download the Repository**

2. **Run the Main Program**

  ```bash
  python main/main.py
  ```

3. **Interact**
  - Press `Enter` to refresh the system information.
  - Enter `s` to trigger the **currently unimplemented** save function.
  - Press `Ctrl+C` to exit the monitor or just close the window.

## Project Structure

  ```txt
  System-Monitor/
  ├── main/
  │   ├── main.py              # Entry point, main loop
  │   ├── gather_info.py       # Gathers system information
  │   ├── display_renderer.py  # Formats and displays info
  │   ├── formatting.py        # Utility formatting functions
  │   └── log_config.py        # Logging configuration (not shown)
  ├── README.md
  ├── other...
  ```

## Notes

  - Sensor information (temperatures, battery) is limited, especially on    Windows.
  - The save functionality is a placeholder and not yet implemented.
  - Designed for cross-platform use, but some features may vary by OS.

## License

This project is provided for educational and personal use. See `LICENSE` if present for details.

---
