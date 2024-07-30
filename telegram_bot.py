import os
import telebot

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message, parse_mode='HTML')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_bot = TelegramBot(telegram_token)

if __name__ == "__main__":
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = "<b>Hello!</b> This is a test message."
    telegram_bot.send_message(chat_id, message)