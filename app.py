# app.py

import os
from crewai import Agent, Task, Process, Crew
from langchain.agents import load_tools
from tools import scrape_reddit

api = os.environ.get("OPENAI_API_KEY")

human_tools = load_tools(["human"])

class Reddit_BrowserTool:
    scrape_reddit = scrape_reddit

explorer = Agent(
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

writer = Agent(
    role="Senior Technical Writer",
    goal="Write engaging and interesting blog posts about the latest AI projects using simple, layman vocabulary",
    backstory="""You are an expert writer on technical innovation, especially in the field of AI and machine learning. You know how to write in
    an engaging, interesting, but simple, straightforward, and concise manner. You know how to present complicated technical terms to the general audience in a
    fun way by using layman words. ONLY use scraped data from the LocalLLama subreddit for the blog.""",
    verbose=True,
    allow_delegation=True
)

critic = Agent(
    role="Expert Writing Critic",
    goal="Provide feedback and criticize blog post drafts. Ensure that the tone and writing style is compelling, simple, and concise",
    backstory="""You are an expert at providing feedback to technical writers. You can identify when a blog text isn't concise,
    simple, or engaging enough. You know how to provide helpful feedback that can improve any text. You ensure that the text
    remains technical and insightful while using layman terms.""",
    verbose=True,
    allow_delegation=True
)

task_report = Task(
    description="""Use and summarize scraped data from subreddit LocalLLama to make a detailed report on the latest rising projects in AI. Use ONLY scraped data from LocalLLama to generate the report. Your final answer MUST be a full analysis report, text only, ignore any code or anything that isn't text. The report has to have bullet points and with 5-10 exciting new AI projects and tools. Write names of every tool and project. Each bullet point MUST contain 3 sentences that refer to one specific AI company, product, model or anything you found on subreddit LocalLLama.""",
    agent=explorer,
    expected_output="""A text-based analysis report with the following structure:
    - Title of the report
    - Introduction
    - Bullet points listing 5-10 new AI projects and tools
      - Each bullet point must include:
        - The name of the AI company, product, or model
        - 3 sentences describing the project or tool
    - Conclusion
    The report should be detailed and concise, summarizing the most exciting new AI projects and tools found on the LocalLLama subreddit."""
)

task_blog = Task(
    description="""Write a blog article with text only and with a short but impactful headline and at least 10 paragraphs. The blog should summarize
    the report on the latest AI tools found on the LocalLLama subreddit. The style and tone should be compelling and concise, fun, technical but also use
    layman words for the general public. Name specific new, exciting projects, apps, and companies in the AI world. Don't
    write "**Paragraph [number of the paragraph]:**", instead start the new paragraph in a new line. Write the names of projects and tools in BOLD.
    ALWAYS include links to the post page. ONLY include information from LocalLLAma.""",

    agent=writer,
    expected_output="""A text-only blog article with the following structure:
    - A short but impactful headline
    - At least 10 paragraphs summarizing the report on AI tools from the LocalLLama subreddit
    - The article should:
      - Be compelling and concise
      - Use layman terms while being fun and technical
      - Highlight new and exciting AI projects, apps, and companies
      - Include the names of projects and tools in bold
      - Include links to projects, tools, and research papers
      - ONLY use information from LocalLLAma
    The format of the blog content should follow this markdown structure:
    ```
    ## [Title of post](link to post)
    - Interesting facts
    - Own thoughts on how it connects to the overall theme of the newsletter
    ## [Title of second post](link to post)
    - Interesting facts
    - Own thoughts on how it connects to the overall theme of the newsletter
    ```"""
)

task_critique = Task(
    description="""The task entails summarizing and critiquing AI projects from the LocalLLama subreddit. The output must be formatted in Markdown and include interesting facts and personal thoughts on how each project connects to the overall theme of the newsletter.""",
    agent=critic,
    output_file='output.md',
    expected_output="""The Output MUST have the following markdown format:
    ```
    ## [Title of post](link to post)
    - Interesting facts
    - Own thoughts on how it connects to the overall theme of the newsletter
    ## [Title of second post](link to post)
    - Interesting facts
    - Own thoughts on how it connects to the overall theme of the newsletter
    ```
    The critique should be compelling and concise, with explanations in layman terms, summarizing AI projects from the LocalLLama subreddit, with sections for interesting facts, key features, and potential impacts."""
)

crew = Crew(
    agents=[explorer, writer, critic],
    tasks=[task_report, task_blog, task_critique],
    verbose=2,
    process=Process.sequential,
)

result = crew.kickoff()

print("######################")
print(result)
