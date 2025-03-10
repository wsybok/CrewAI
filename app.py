import os
from dotenv import load_dotenv
from crewai import Process, Crew
from agents import CrewAgents
from tasks import CrewTasks
from telegram_bot import TelegramBot
from telegraph import Telegraph, TelegraphException
from bs4 import BeautifulSoup



load_dotenv()

api = os.environ.get("OPENAI_API_KEY")


agents = CrewAgents()
tasks = CrewTasks()

crew = Crew(
    agents=[agents.explorer(), agents.writer(), agents.critic(), agents.telegra_writer()],
    tasks=[tasks.task_report(), tasks.task_blog(), tasks.task_critique(), tasks.task_telegra()],
    verbose=2,
    process=Process.sequential,
)

result = crew.kickoff()

report_file_path = "research_report1.html"

# Read the content of the HTML report file
with open(report_file_path, "r", encoding="utf-8") as file:
    html_report = file.read()

# Use BeautifulSoup to parse the HTML and extract the body content
soup = BeautifulSoup(html_report, 'html.parser')
allowed_tags = ['a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure', 'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's', 'strong', 'u', 'ul', 'video']

# Filter out disallowed tags
for tag in soup.find_all(True):
    if tag.name not in allowed_tags:
        tag.unwrap()

# Convert the filtered content back to a string
html_content = str(soup)
print("######################")
print(result)


# Initialize Telegraph and create an account
telegraph = Telegraph()
telegraph.create_account(short_name='your_bot_name')

# Create a Telegraph page with the HTML report
response = telegraph.create_page(
    title='Research Report',
    html_content=html_report
)

# Get the URL of the created page
telegraph_url = 'https://telegra.ph/{}'.format(response['path'])

# Send the Telegraph URL to Telegram
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
telegram_bot = TelegramBot(telegram_token)
telegram_bot.send_message(chat_id, f"Here is the research report: {telegraph_url}")