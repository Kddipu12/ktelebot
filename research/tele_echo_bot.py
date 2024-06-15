import logging
from aiogram import Bot,Dispatcher,executor,types
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("TOKEN")
# print(API_TOKEN)

#cofigure logging
logging.basicConfig(level=logging.INFO)

#iniatialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp=Dispatcher(bot)

@dp.message_handler(commands=['start','help'])
async def command_start_handler(message: types.Message):
    '''
    This handler receives messages with '/start ' or '/help' command

    '''
    await message.reply(f"Hi\n I am Kd's Favourite bot!\nPowered by aiogram.")

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)