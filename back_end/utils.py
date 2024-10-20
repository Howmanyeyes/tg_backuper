"""This module has utilities that are used throughout the project"""

import logging
from functools import wraps
import asyncio
import sys
import json

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


def backend_answer(func):
    """Function to answer backend requests in specific format"""
    template = AnswerTemplate()
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            template.data = result
            return template
        except Exception as e:
            template.status = "ERROR"
            template.data = str(e)
            return template

    return wrapper

class AnswerTemplate:
    """Class for easy answer template"""
    def __init__(self):
        self.template = {
            "status": "GOOD",
            "data": None
        }

    def __repr__(self):
        return f"\"status\": \"{self.status}\", \"data\": {str(json.loads(self.data))}"

    @property
    def data(self):
        """Returns data from template as a property"""
        return self.template["data"]

    @data.setter
    def data(self, new_data):
        """Sets data to template"""
        self.template["data"] = new_data

    @property
    def status(self):
        """Returns status from template as a property"""
        return self.template["status"]

    @status.setter
    def status(self, new_status):
        """Sets status to template"""
        self.template["status"] = new_status
