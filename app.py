import os
from crewai import Process, Crew
from agents import CrewAgents
from tasks import CrewTasks

api = os.environ.get("OPENAI_API_KEY")


crew = Crew(
    agents=[explorer, writer, critic],
    tasks=[task_report, task_blog, task_critique],
    verbose=2,
    process=Process.sequential,
)

result = crew.kickoff()

print("######################")
print(result)
