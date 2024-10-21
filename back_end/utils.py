"""This module has utilities that are used throughout the project"""

import logging
from functools import wraps
import asyncio
import sys
import json

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

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
            1/0
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong: {e}") from e

    return wrapper
