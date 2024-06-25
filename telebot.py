from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai

class Reference:
    '''
    A class to store previous responses from the chatgpt api
    '''
    def __init__(self) -> None:
        self.response = ""

load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TOKEN")

# model name
MODEL_NAME = "gpt-3.5-turbo"

# initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    '''
    A function to clear the previous conversation and context
    '''
    reference.response = ""

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    '''
    This handler receives messages with '/start' or '/help' command
    '''
    clear_past()
    await message.reply(f"Hi\n I am Kd's Favourite bot!\nHow can I assist you?")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display help menu
    """
    help_command = """
    HI THERE, I'm ChatGPT Telegram bot created by KD! Please follow these commands -
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help - to get this help menu.
    I hope this helps :)
    """
    await message.reply(help_command)

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the past conversation and context
    """
    clear_past()
    await message.reply("Previous conversation and context cleared!")

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the ChatGPT API.
    """
    print(f">>> USER:\n \t{message.text}")
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.text}
            ]
        )
        reference.response = response.choices[0].message["content"]
        print(f">>> chatGPT:\n \t{reference.response}")
        await bot.send_message(chat_id=message.chat.id, text=reference.response)
    except Exception as e:
        print(f"Error: {e}")
        await bot.send_message(chat_id=message.chat.id, text="Sorry, something went wrong. Please try again later.")

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
