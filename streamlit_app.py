import os
from dotenv import load_dotenv
from crewai import Process, Crew
from agents import CrewAgents
from tasks import CrewTasks
from telegram_bot import TelegramBot
from telegraph import Telegraph
from bs4 import BeautifulSoup
import streamlit as st
from tools.Reddit_BrowserTool import RedditBrowserTool

def load_configuration():
    load_dotenv()
    return {
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "telegram_token": os.getenv("TELEGRAM_BOT_TOKEN"),
        "chat_id": os.getenv("TELEGRAM_CHAT_ID")
    }

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
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def filter_html_content(html_content, allowed_tags):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
    return str(soup)

def create_telegraph_page(telegraph, title, html_content):
    response = telegraph.create_page(title=title, html_content=html_content)
    return 'https://telegra.ph/{}'.format(response['path'])

def send_telegram_message(telegram_bot, chat_id, message):
    telegram_bot.send_message(chat_id, message)

def main():
    st.title("Research Report Generator")

    subreddit_name = st.sidebar.text_input("Enter Subreddit Name", value="LocalLLaMA")

    if st.button("Generate Report", key="generate_report_button"):
        config = load_configuration()
        crew = initialize_crew()

        # Display progress and AI thinking process
        chat_box = st.chat_message("AI Assistant")
        chat_box.write("Initializing Crew...")

        result = crew.kickoff()
        chat_box.write("Crew kickoff complete. Generating report...")

        # Scrape Reddit content
        reddit_tool = RedditBrowserTool()
        scraped_data = reddit_tool.scrape_reddit(subreddit_name)
        chat_box.write(f"Scraped data from subreddit: {subreddit_name}")

        # Process and generate report
        report_file_path = "research_report.html"
        html_report = read_html_report(report_file_path)
        chat_box.write("Report generated. Filtering HTML content...")

        allowed_tags = ['a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure', 'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's', 'strong', 'u', 'ul', 'video']
        filtered_html_content = filter_html_content(html_report, allowed_tags)
        chat_box.write("HTML content filtered. Creating Telegraph page...")

        telegraph = Telegraph()
        telegraph.create_account(short_name='your_bot_name')
        telegraph_url = create_telegraph_page(telegraph, 'Research Report', filtered_html_content)
        chat_box.write("Telegraph page created. Sending to Telegram...")

        telegram_bot = TelegramBot(config['telegram_token'])
        send_telegram_message(telegram_bot, config['chat_id'], f"Here is the research report: {telegraph_url}")

        chat_box.write("Report generated and sent to Telegram!")
        st.success("Report generated and sent to Telegram!")
        st.write(f"Telegraph URL: {telegraph_url}")

        # Print scraped data to console
        print(scraped_data)

        # Display scraped data in Streamlit UI
        st.write("Scraped Reddit Data:")
        st.json(scraped_data)

if __name__ == "__main__":
    main()