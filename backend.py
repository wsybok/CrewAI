from flask import Flask, request, jsonify
from crewai import Process, Crew
from agents import CrewAgents
from tasks import CrewTasks
from telegram_bot import TelegramBot
from telegraph import Telegraph
from bs4 import BeautifulSoup
from tools.Reddit_BrowserTool import RedditBrowserTool
from config import allowed_tags, config  # Import allowed_tags and config
import os

app = Flask(__name__)

def initialize_crew():
    agents = CrewAgents()
    tasks = CrewTasks()
    return Crew(
        agents=[agents.explorer(), agents.writer(), agents.critic(), agents.telegra_writer()],
        tasks=[tasks.task_report(), tasks.task_blog(), tasks.task_critique()],
        verbose=2,
        process=Process.sequential,
    )

def read_html_report(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        return file.read()

def filter_html_content(html_content, allowed_tags):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
    return str(soup)

def remove_unwanted_tags(html_content, unwanted_tags):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in unwanted_tags:
        for match in soup.findAll(tag):
            match.unwrap()
    return str(soup)

def create_telegraph_page(telegraph, title, html_content):
    try:
        response = telegraph.create_page(title=title, html_content=html_content)
        return 'https://telegra.ph/{}'.format(response['path'])
    except Exception as e:
        raise Exception(f"Error creating Telegraph page: {e}")

def send_telegram_message(telegram_bot, chat_id, message):
    telegram_bot.send_message(chat_id, message)

def clean_text(text):
    """ Clean the text to remove invalid characters """
    return text.encode('utf-8', 'replace').decode('utf-8')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    subreddit_name = request.json.get('subreddit_name')
    crew = initialize_crew()
    result = crew.kickoff()
    reddit_tool = RedditBrowserTool()
    scraped_data = reddit_tool.scrape_reddit(subreddit_name)
    report_file_path = "research_report.html"
    html_report = read_html_report(report_file_path)
    filtered_html_content = filter_html_content(html_report, allowed_tags)
    filtered_html_content = remove_unwanted_tags(filtered_html_content, ['h1', 'h2'])
    return jsonify({"filtered_html_content": filtered_html_content})

@app.route('/send_report', methods=['POST'])
def send_report():
    edited_report = request.json.get('edited_report')
    telegraph = Telegraph()
    telegraph.create_account(short_name='your_bot_name')
    final_html_content = remove_unwanted_tags(edited_report, ['h1', 'h2'])
    final_html_content = clean_text(final_html_content)
    telegraph_url = create_telegraph_page(telegraph, 'Research Report', final_html_content)
    telegram_bot = TelegramBot(config['telegram_token'])
    send_telegram_message(telegram_bot, config['chat_id'], f"Here is the research report: {telegraph_url}")
    return jsonify({"telegraph_url": telegraph_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)