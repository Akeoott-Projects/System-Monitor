# gather_info.py for fetching system resources only.

GATHER_INFO_FILE_VERSION = "1.0.0"

from log_config import log
import platform
import psutil
import time

active_log = True

class GatherSystemInfo:
    def __init__(self):
        # Enable logging for initialization
        self.active_log = active_log
        if self.active_log: log.info("INFO: logging in class `GatherSystemInfo` is now temporarily on to prevent repetition later.")
        if self.active_log: log.info("Initialized GatherSystemInfo")
        # Initialize data containers
        self.cpu     = {}
        self.memory  = {}
        self.disks   = []
        self.network = []
        self.sensors = {}
        self.other   = {}

        # Prime psutil for more accurate readings
        psutil.cpu_percent(interval=None)
        psutil.net_io_counters(pernic=True, nowrap=True)

        # Small delay to allow counters to update
        time.sleep(0.1)

    def gather_cpu(self):
        # Gather CPU statistics
        cpu_count = psutil.cpu_count(logical=True)
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_times_percent = psutil.cpu_times_percent(interval=None)._asdict()
        cpu_times = psutil.cpu_times(percpu=False)._asdict()
        cpu_stats = psutil.cpu_stats()._asdict()
        cpu_freq = psutil.cpu_freq(percpu=False)._asdict()
        
        self.cpu = {
            "cpu_count": {
                "count": cpu_count,
            },
            "cpu_percent": {
                "percent": cpu_percent,
            },
            "cpu_times_percent": cpu_times_percent,
            "cpu_times": cpu_times,
            "cpu_stats": cpu_stats,
            "cpu_freq": cpu_freq,
        }
        if self.active_log: log.info("Fetched CPU info.")

    def gather_memory(self):
        # Gather memory statistics
        virtual_memory = psutil.virtual_memory()._asdict()
        swap_memory = psutil.swap_memory()._asdict()
        self.memory = {
            "virtual_memory": virtual_memory,
            "swap_memory": swap_memory,
        }
        if self.active_log: log.info("Fetched memory info.")

    def gather_disks(self):
        # Gather disk usage for all physical partitions
        partitions = psutil.disk_partitions(all=False) # Only physical devices
        disk_usages = []
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                disk_usages.append({
                    "device": p.device,
                    "mountpoint": p.mountpoint,
                    "fstype": p.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                })
            except Exception as e:
                if self.active_log: log.warning(f"Could not get disk usage for {p.mountpoint}: {type(e).__name__}: {e}")
        self.disks = disk_usages
        if self.active_log: log.info("Fetched disk info.")

    def gather_network(self):
        # Gather network statistics for each interface
        net_io = psutil.net_io_counters(pernic=True, nowrap=True) # Per network interface
        net_stats = psutil.net_if_stats() # Network interface status (up/down, speed)
        net_addrs = psutil.net_if_addrs() # Network interface addresses (IPs)

        network_info = []
        for interface_name, counters in net_io.items():
            stats = net_stats.get(interface_name)
            addrs = net_addrs.get(interface_name, [])

            network_info.append({
                "interface": interface_name,
                "bytes_sent": counters.bytes_sent,
                "bytes_recv": counters.bytes_recv,
                "packets_sent": counters.packets_sent,
                "packets_recv": counters.packets_recv,
                "errin": counters.errin,
                "errout": counters.errout,
                "dropin": counters.dropin,
                "dropout": counters.dropout,
                "is_up": stats.isup if stats else "N/A",
                "speed_mbps": stats.speed if stats else "N/A",
                "addresses": [{"family": str(addr.family), "address": addr.address, "netmask": addr.netmask, "broadcast": addr.broadcast} for addr in addrs]
            })
        self.network = network_info
        if self.active_log: log.info("Fetched network info.")

    def gather_sensors(self):
        # Sensors not implemented (especially on Windows)
        self.sensors = {
            "NOTE": "Currently empty as on windows, its mostly empty and i cannot make this work anyway.",
        }
        if self.active_log: log.warning("Fetching sensors is currently off due to it not working.")

    def gather_other(self):
        # Gather OS and user information
        boot_time = psutil.boot_time()
        users = psutil.users()
        
        self.other = {
            "os_name": platform.system(),
            "os_version": platform.release(),
            "boot_time_timestamp": boot_time,
            "boot_time_readable": time.ctime(boot_time),
            "current_users": [{"name": u.name, "host": u.host, "started": time.ctime(u.started)} for u in users],
        }

    def system_info(self):
        """
        Gathers all system information as a fresh snapshot.
        Call this method repeatedly in your main loop to get updated data.
        """
        self.gather_cpu()
        self.gather_memory()
        self.gather_disks()
        self.gather_network()
        self.gather_sensors()
        self.gather_other()

        info = {
            "timestamp": time.time(),
            "cpu": self.cpu,
            "memory": self.memory,
            "disks": self.disks,
            "network": self.network,
            "sensors": self.sensors,
            "other": self.other,
        }
        if self.active_log: log.info("Returned info to main.")
        if self.active_log: log.info("INFO: Logging inside class `GatherSystemInfo` is now off to prevent large repetitions.")
        self.active_log = False
        return info
    
if False:
    if __name__ == "__main__":
        import json
        a = GatherSystemInfo()
        info = a.system_info()
        print(json.dumps(info, indent=2))