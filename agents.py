import os
from crewai import Agent
from tools.Reddit_BrowserTool import RedditBrowserTool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

reddit_tool = RedditBrowserTool()
human_tools = load_tools(["human"])

# call gemini model
llm_gemini = ChatGoogleGenerativeAI(model='gemini-1.5-pro-exp-0801',
                            temperature=0.1,
                            verbose = True,
                            goggle_api_key=os.getenv('GOOGLE_API_KEY')
                            )   

class CrewAgents:
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
            llm = llm_gemini,
            #llm=ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0.7),
            tools=[reddit_tool.scrape_reddit]
        )

    def writer(self):
        return Agent(
            role="Senior Technical Writer",
            goal="Write engaging and interesting blog posts about the latest AI projects using simple, layman vocabulary",
            backstory="""You are an expert writer on technical innovation, especially in the field of AI and machine learning. You know how to write in
            an engaging, interesting, but simple, straightforward, and concise manner. You know how to present complicated technical terms to the general audience in a
            fun way by using layman words. ONLY use scraped data from the LocalLLama subreddit for the blog.""",
            verbose=True,
            llm = llm_gemini,
            #llm=ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0.7),
            allow_delegation=False
        )

    def critic(self):
        return Agent(
            role="Expert Writing Critic",
            goal="Provide feedback and criticize blog post drafts. Ensure that the tone and writing style is compelling, simple, and concise",
            backstory="""You are an expert at providing feedback to technical writers. You can identify when a blog text isn't concise,
            simple, or engaging enough. You know how to provide helpful feedback that can improve any text. You ensure that the text
            remains technical and insightful while using layman terms.""",
            verbose=True,
            llm = llm_gemini,
            #llm=ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0.7),
            allow_delegation=False
        )
    
    def telegra_writer(self):
        return Agent(
            role="'Telegra Writer'",
            goal="Rewrit the report so the report is suitable for a telegraph page",
            backstory="""You are skilled in writing reports that are perfectly formatted for telegra. Your goal is to ensure that all reports adhere to the telegra formatting guidelines. telegra only Available tags: a, aside, b, blockquote, br, code, em, figcaption, figure, h3, h4, hr, i, iframe, img, li, ol, p, pre, s, strong, u, ul, video. """,
            verbose=True,
            llm=llm_gemini,
            #llm=ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0.7),
            allow_delegation=False
        )