# formatting.py just for makin things look normal.

import time
from datetime import datetime
import psutil

def bytes_to_human_readable(n_bytes):
    """Convert bytes to a human-readable format (e.g., KB, MB, GB)."""
    if n_bytes is None:
        return "N/A"
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i * 10)
    
    for s in reversed(symbols):
        if n_bytes >= prefix[s]:
            value = float(n_bytes) / prefix[s]
            return f"{value:.2f}{s}"

    return f"{n_bytes}B"

def seconds_to_human_readable(seconds):
    """Converts seconds to a human-readable format (H:MM:SS)."""
    if seconds == psutil.POWER_TIME_UNLIMITED:
        return "Unlimited"
    if seconds == psutil.POWER_TIME_UNKNOWN:
        return "Unknown"
    
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h)}h {int(m)}m {int(s)}s"

def timestamp_to_datetime_str(timestamp):
    """Converts a Unix timestamp to a human-readable date and time string."""
    if timestamp is None:
        return "N/A"
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')