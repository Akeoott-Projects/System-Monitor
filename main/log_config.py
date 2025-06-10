# logging_setup.py for configuring logging via the akeoott_logging_config library.

LOGGING_SETUP_FILE_VERSION = "1.0.0"

from akeoott_logging_config import LogConfig
import logging

def setup():
    # Set up logging configuration using akeoott_logging_config
    log = LogConfig(logger_name="main")
    log.setup(
        activate_logging=True,
        print_log=False,
        save_log=True,
        log_file_path="main",
        log_file_name="system_monitor_logs.log",
        log_level=logging.DEBUG,
        log_format='%(levelname)s (%(asctime)s.%(msecs)03d)     %(message)s [Line: %(lineno)d in %(filename)s - %(funcName)s]',
        date_format='%Y-%m-%d %H:%M:%S',
        log_file_mode='w'
    )
    return log.logger

log = setup()