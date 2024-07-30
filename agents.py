from crewai import Agent
from tools.Reddit_BrowserTool import

class CrewAgents():
  def explorer(self):
    return Agent(
        role="Senior Researcher",
    goal="Find and explore the most exciting projects and companies on LocalLLama subreddit in 2024",
    backstory="""You are an expert strategist who knows how to spot emerging trends and companies in AI, tech, and machine learning.
    You're great at finding interesting, exciting projects on the LocalLLama subreddit. You turn scraped data into detailed reports with names
    of the most exciting projects and companies in the AI/ML world. ONLY use scraped data from the LocalLLama subreddit for the report.
    """,
    verbose=True,
    allow_delegation=False,
    tools=[BrowserTool().scrape_reddit] + human_tools
)

def writer(self):
    return Agent(
    role="Senior Technical Writer",
    goal="Write engaging and interesting blog posts about the latest AI projects using simple, layman vocabulary",
    backstory="""You are an expert writer on technical innovation, especially in the field of AI and machine learning. You know how to write in
    an engaging, interesting, but simple, straightforward, and concise manner. You know how to present complicated technical terms to the general audience in a
    fun way by using layman words. ONLY use scraped data from the LocalLLama subreddit for the blog.""",
    verbose=True,
    allow_delegation=True
)

def critic(self):
    return Agent(
    role="Expert Writing Critic",
    goal="Provide feedback and criticize blog post drafts. Ensure that the tone and writing style is compelling, simple, and concise",
    backstory="""You are an expert at providing feedback to technical writers. You can identify when a blog text isn't concise,
    simple, or engaging enough. You know how to provide helpful feedback that can improve any text. You ensure that the text
    remains technical and insightful while using layman terms.""",
    verbose=True,
    allow_delegation=True
)
