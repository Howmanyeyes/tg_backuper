"""This module has utilities that are used throughout the project"""

import logging
from functools import wraps
import asyncio
import sys

from fastapi.responses import Response

logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(message)s',
datefmt='%d-%m-%Y %H:%M:%S',
handlers=[
    logging.FileHandler('all_logs.log', encoding='utf-8', mode='a'),
    logging.StreamHandler(sys.stdout)
    ]
)

def log_this(func):
    """Logs message with time and level"""
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                logging.info("Function %s finished with result %r", func.__name__, result)
                return result
            except Exception as e:
                logging.exception("Function %s finished with error %s", func.__name__, e)
                raise
        return wrapper

    @wraps(func)
    def wrapper_non_as(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logging.info("Function %s finished with result %r", func.__name__, result)
            return result
        except Exception as e:
            logging.exception("Function %s finished with error %s", func.__name__, e)
            raise
    return wrapper_non_as


def backend_answer(func): # TODO rework to industry standard 
    """Function to answer backend requests in specific format"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return Response(status_code=500, content=f"Something went wrong during excecution of\
decorator backend_answer while wrapping function {func.__name__}. Exception: {e}")
    return wrapper

def filter_settings(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            try:
                links = (await kwargs['request'].json())['files']
            except Exception as e:
                logging.exception("Something went wrong during excecution of filter_settings while wrapping function %s. Exception: %s", func.__name__, e)
                return Response(status_code=500, content=f"Something went wrong during excecution of\
filter_settings while wrapping function {func.__name__}. Exception: {e}")
            
            return await func(*args, **kwargs)
        except Exception as e:
            return Response(status_code=500, content=f"Something went wrong during excecution of\
decorator backend_answer while wrapping function {func.__name__}. Exception: {e}")
    return wrapper

def smart_compress(link):
    """Compreses file provided by it's link into (multiple part) 7z archive"""
