# app.py

import os
from crewai import Agent, Task, Process, Crew
from langchain.agents import load_tools
from tools import scrape_reddit

api = os.environ.get("OPENAI_API_KEY")

human_tools = load_tools(["human"])

class Reddit_BrowserTool:
    scrape_reddit = scrape_reddit

crew = Crew(
    agents=[explorer, writer, critic],
    tasks=[task_report, task_blog, task_critique],
    verbose=2,
    process=Process.sequential,
)

result = crew.kickoff()

print("######################")
print(result)
