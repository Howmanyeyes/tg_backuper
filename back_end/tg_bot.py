from aiogram import Bot
import asyncio
from aiogram.types import BufferedInputFile
from config import config



bot = Bot(config.api)
# 417766628 my id
# reply_document(file)

async def main():
    doc = BufferedInputFile(filename='back_end/main.py', file = open('back_end/main.py', 'rb'))
    await bot.send_document(chat_id = 417766628, document=doc)

if __name__ == '__main__':
    asyncio.run(main())