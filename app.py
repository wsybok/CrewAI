import os
from crewai import Agent, Task, Process, Crew
from langchain_community.agent_toolkits.load_tools import load_tools
from agents import explorer, writer, critic
from tasks import task_report, task_blog, task_critique

api = os.environ.get("OPENAI_API_KEY")

human_tools = load_tools(["human"])

crew = Crew(
    agents=[explorer, writer, critic],
    tasks=[task_report, task_blog, task_critique],
    verbose=2,
    process=Process.sequential,
)

result = crew.kickoff()

print("######################")
print(result)
