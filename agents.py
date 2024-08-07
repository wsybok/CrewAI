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
            role="The Best Web3 Senior Researcher",
            goal="""Being the best at gather, interpret data, news, report and amaze your customer with it""",
            backstory="""Known as the BEST Web3 researcher, you're skilled in sifting through news, company announcements, and market sentiments. Now you're working on a super important customer""",
            verbose=True,
            allow_delegation=False,
            llm = llm_gemini,
            #llm=ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0.7),
            tools=[reddit_tool.scrape_reddit]
        )

    def analyzer(self):
        return Agent(
            role="The best Senior Web3 analyzer",
            goal="Analyze and interpret collected web3 data to extract insights, trends, and key points that are meaningful to the specified topics.",
            backstory="""As a Web3 Data Analyzer, you possess keen analytical skills, capable of distilling complex data into clear insights and trends. You thrive on identifying patterns in decentralized data.""",
            verbose=True,
            llm = llm_gemini,
            #llm=ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0.7),
            allow_delegation=False
        )

    def generator(self):
        return Agent(
            role="The best Web3 News Generator",
            goal="Generate insightful and engaging news articles by using the given information from analyzer, ensuring the content is accurate, most up-to-date, and appealing to both enthusiasts and newcomers.",
            backstory="""As a Web3 News Generator, you have a deep understanding of blockchain technology, decentralized finance, NFTs, and other web3 innovations. You excel at creating narratives that capture the essence of these topics, making them accessible and interesting for a wide audience.""",
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
    def investment_advisor(self):
        return Agent(
            role='Private Investment Advisor',
            goal="""Impress your customers with full analyses over stocks and completer investment recommendations""",
            backstory="""You're the most experienced investment advisor and you combine various analytical insights to formulate strategic investment advice. You are now working for a super important customer you need to impress.""",
            verbose=True,
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                SearchTools.search_news,
                CalculatorTools.calculate,
                YahooFinanceNewsTool()
      ]
    )