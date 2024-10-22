"""Module for tg bot"""
import time
import asyncio
from aiogram import Bot
from aiogram.types import BufferedInputFile
from config import config
import logging
import sys
import asyncio
from functools import wraps
from json_log_formatter import JSONFormatter

async def send_document(chat_id, document):
    await bot.send_document(chat_id=chat_id, document=document)

bot = Bot(config.api) # 417766628 my id


async def main():
    with open('back_end/im.png', 'rb') as f:
        file_data = f.read()
    doc = BufferedInputFile(filename='back_end/el.png', file = file_data)
    await send_document(417766628, doc)

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('app_logs.json', mode='a', encoding='utf-8')
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = JSONFormatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger







if __name__ == '__main__':
    asyncio.run(main())