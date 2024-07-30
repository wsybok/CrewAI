import os
from dotenv import load_dotenv
from crewai import Process, Crew
from agents import CrewAgents
from tasks import CrewTasks

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

print("######################")
print(result)
