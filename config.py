# config.py

import os
from dotenv import load_dotenv

load_dotenv()

allowed_tags = [
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure', 
    'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's', 'strong', 
    'u', 'ul', 'video'
]

config = {
    #"api_key": os.environ.get("OPENAI_API_KEY"),
    "telegram_token": os.getenv("TELEGRAM_BOT_TOKEN"),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID")
}