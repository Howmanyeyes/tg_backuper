"""This module has utilities that are used throughout the project"""

import logging
from functools import wraps
import asyncio
import sys

from fastapi.responses import Response



def log_this(level=logging.INFO):
    """Decorator for leveled logging"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            extra = {'function': func.__name__, 'args': args, 'kwargs': kwargs}
            try:
                result = await func(*args, **kwargs)
                logger.log(level, "Function finished successfully", extra=extra)
                return result
            except Exception as e:
                extra.update({'error': str(e)})
                logger.exception("Function raised an exception", extra=extra)
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            extra = {'function': func.__name__, 'args': args, 'kwargs': kwargs}
            try:
                result = func(*args, **kwargs)
                logger.log(level, "Function finished successfully", extra=extra)
                return result
            except Exception as e:
                extra.update({'error': str(e)})
                logger.exception("Function raised an exception", extra=extra)
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator



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
