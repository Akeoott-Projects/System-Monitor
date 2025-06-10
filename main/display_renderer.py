# display_renderer.py just for display.

from formatting import bytes_to_human_readable, seconds_to_human_readable, timestamp_to_datetime_str
from tabulate import tabulate
import os

class DisplayRenderer:
    def __init__(self, table_format="fancy_grid"):
        # Initialize the renderer with a table format for tabulate
        self.table_format = table_format

    def clear_screen(self):
        """Clears the terminal screen."""
        # Use 'cls' for Windows, 'clear' for Unix-like systems
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_system_info(self, info_data):
        """Main method to render all system information."""
        self.clear_screen()

        # Display a header with current timestamp
        current_time_str = timestamp_to_datetime_str(info_data.get("timestamp"))
        print(f"--- System Monitor - {current_time_str} ---")
        print("-" * 50)

        # Call individual displays for each section
        self._render_cpu_info(info_data.get("cpu", {}))
        self._render_memory_info(info_data.get("memory", {}))
        self._render_disks_info(info_data.get("disks", []))
        self._render_network_info(info_data.get("network", []))
        self._render_sensors_info(info_data.get("sensors", {}))
        self._render_other_info(info_data.get("other", {}))

        print("\n" + "=" * 50)
        print("Press Ctrl+C to stop.")

    def _render_cpu_info(self, cpu_data):
        """Renders formatted CPU information."""
        print("\n## CPU Information")
        if not cpu_data:
            print("  No CPU data available.")
            return

        # Display logical CPU count and overall usage
        print(f"  CPU Count (Logical): {cpu_data.get('cpu_count', {}).get('count', 'N/A')}")
        print(f"  Overall Usage: {cpu_data.get('cpu_percent', {}).get('percent', 'N/A'):.1f}%")

        # Display CPU times in seconds
        cpu_times = cpu_data.get('cpu_times', {})
        if cpu_times:
            print("  Times (seconds):")
            for key, val in cpu_times.items():
                print(f"    - {key.capitalize()}: {val:.2f}s")

        # Display CPU times as percentages
        cpu_times_percent = cpu_data.get('cpu_times_percent', {})
        if cpu_times_percent:
            print("  Times (%):")
            for key, val in cpu_times_percent.items():
                print(f"    - {key.capitalize()}: {val:.1f}%")
        print("-" * 50)

    def _render_memory_info(self, memory_data):
        """Renders formatted Memory information."""
        print("\n## Memory Information")
        if not memory_data:
            print("  No Memory data available.")
            return

        # Display virtual memory stats
        virtual_mem = memory_data.get('virtual_memory', {})
        if virtual_mem:
            print("  Virtual Memory:")
            print(f"    Total:     {bytes_to_human_readable(virtual_mem.get('total'))}")
            print(f"    Available: {bytes_to_human_readable(virtual_mem.get('available'))}")
            print(f"    Used:      {bytes_to_human_readable(virtual_mem.get('used'))} ({virtual_mem.get('percent', 'N/A'):.1f}%)")
            print(f"    Free:      {bytes_to_human_readable(virtual_mem.get('free'))}")

        # Display swap memory stats
        swap_mem = memory_data.get('swap_memory', {})
        if swap_mem:
            print("  Swap Memory:")
            print(f"    Total: {bytes_to_human_readable(swap_mem.get('total'))}")
            print(f"    Used:  {bytes_to_human_readable(swap_mem.get('used'))} ({swap_mem.get('percent', 'N/A'):.1f}%)")
            print(f"    Free:  {bytes_to_human_readable(swap_mem.get('free'))}")
        print("-" * 50)

    def _render_disks_info(self, disks_data):
        """Renders formatted Disk information using tabulate."""
        print("\n## Disk Information")
        if not disks_data:
            print("  No Disk data available.")
            return

        # Prepare table headers and rows for disk info
        table_headers = ["Device", "Mount Point", "FS Type", "Total", "Used", "Free", "Usage %"]
        table_rows = []
        for disk in disks_data:
            table_rows.append([
                disk.get("device", "N/A"),
                disk.get("mountpoint", "N/A"),
                disk.get("fstype", "N/A"),
                bytes_to_human_readable(disk.get("total")),
                bytes_to_human_readable(disk.get("used")),
                bytes_to_human_readable(disk.get("free")),
                f"{disk.get('percent', 'N/A'):.1f}%" if isinstance(disk.get('percent'), (int, float)) else "N/A"
            ])
        
        # Print disk info as a formatted table
        print(tabulate(table_rows, headers=table_headers, tablefmt=self.table_format))
        print("-" * 50)

    def _render_network_info(self, network_data):
        """Renders formatted Network information using tabulate."""
        print("\n## Network Information")
        if not network_data:
            print("  No Network data available.")
            return

        # Prepare table headers and rows for network info
        table_headers = ["Interface", "Status", "Speed", "Sent", "Received"]
        table_rows = []
        for net_if in network_data:
            table_rows.append([
                net_if.get("interface", "N/A"),
                "Up" if net_if.get("is_up") == True else "Down" if net_if.get("is_up") == False else "N/A",
                f"{net_if.get('speed_mbps', 'N/A')} Mbps",
                bytes_to_human_readable(net_if.get("bytes_sent")),
                bytes_to_human_readable(net_if.get("bytes_recv"))
            ])
        
        # Print network info as a formatted table
        print(tabulate(table_rows, headers=table_headers, tablefmt=self.table_format))
        print("-" * 50)

    def _render_sensors_info(self, sensors_data):
        """Renders formatted Sensor information."""
        print("\n## Sensor Information")
        # If only NOTE is present, display the note
        if not sensors_data or (len(sensors_data) == 1 and "NOTE" in sensors_data):
            print(f"  Note: {sensors_data.get('NOTE', 'No sensor data available or functional on this OS.')}")
        else:
            # CURRENTLY NOT IN USE!
            # Display temperature sensors if available
            if sensors_data.get("temperatures"):
                print("  Temperatures:")
                for name, entries in sensors_data["temperatures"].items():
                    print(f"    {name}:")
                    for entry in entries:
                        print(f"      - Label: {entry.label}, Current: {entry.current}°C")
            # Display battery info if available
            if sensors_data.get("battery"):
                battery = sensors_data["battery"]
                print("  Battery:")
                print(f"    Percent: {battery.percent:.1f}%")
                print(f"    Power Plugged: {battery.power_plugged}")
                print(f"    Time Left: {seconds_to_human_readable(battery.secsleft)}")
        print("-" * 50)

    def _render_other_info(self, other_data):
        """Renders other general system information."""
        print("\n## Other Information")
        if not other_data:
            print("  No Other data available.")
            return

        # Display OS name and version
        print(f"  OS: {other_data.get('os_name', 'N/A')} {other_data.get('os_version', 'N/A')}")
        print(f"  Boot Time: {timestamp_to_datetime_str(other_data.get('boot_time_timestamp'))}")
        
        # Display currently logged-in users
        users = other_data.get('current_users', [])
        if users:
            print("  Logged-in Users:")
            for user in users:
                print(f"    - {user.get('name', 'N/A')} (Host: {user.get('host', 'N/A')}, Started: {user.get('started', 'N/A')})")
        print("-" * 50)