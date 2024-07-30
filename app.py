import os
from dotenv import load_dotenv
from crewai import Process, Crew
from agents import CrewAgents
from tasks import CrewTasks
from telegram_bot import TelegramBot
from telegraph import Telegraph, TelegraphException



load_dotenv()

api = os.environ.get("OPENAI_API_KEY")


agents = CrewAgents()
tasks = CrewTasks()

crew = Crew(
    agents=[agents.explorer(), agents.writer(), agents.critic()],
    tasks=[tasks.task_report(), tasks.task_blog(), tasks.task_critique()],
    verbose=2,
    process=Process.sequential,
)

result = crew.kickoff()

report_file_path = "research_report.html"

# Read the content of the HTML report file
with open(report_file_path, "r", encoding="utf-8") as file:
    html_report = file.read()


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