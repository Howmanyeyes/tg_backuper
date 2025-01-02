from logstash_async.handler import AsynchronousLogstashHandler
import logging
import socket
import sys
from typing import Optional

def setup_logger():
    """Sets up a logger that logs to a file, console, and logstash"""
    logger = logging.getLogger('python-logstash-logger')
    logger.setLevel(logging.INFO)

    # Set up handlers for file, console, and Logstash (with modified host field)
    file_handler = logging.FileHandler('bot_logs.log', mode='a', encoding='utf-8')
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Asynchronous handler for Logstash
    async_handler = AsynchronousLogstashHandler(
        host="localhost",
        port=5000,
        database_path=None
    )

    # Format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(async_handler)
    return logger

def logmsg(message="No message", **kwargs):
    # Form the log message with the specified fields
    return f'{message} • ' + ', '.join(f'{k}: {v}' for k, v in kwargs.items() if v is not None)

if __name__ == "__main__":
    # Initialize the logger
    logger = setup_logger()
    
    # Send a sample log with a custom message structure
    logger.info(extra = logmsg(message="test", data=1, beta=2))
