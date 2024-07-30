from crewai import Task
from textwrap import dedent
from agents import CrewAgents

class CrewTasks:
    def task_report(self):
        return Task(
            description=dedent("""
            Use and summarize scraped data from subreddit LocalLLama to make a detailed report on the latest rising projects in AI. Use ONLY scraped data from LocalLLama to generate the report. Your final answer MUST be a full analysis report, text only, ignore any code or anything that isn't text. The report has to have bullet points and with 5-10 exciting new AI projects and tools. Write names of every tool and project. Each bullet point MUST contain 3 sentences that refer to one specific AI company, product, model or anything you found on subreddit LocalLLama.
            """),
            agent=CrewAgents().explorer(),
            expected_output=dedent("""
            A text-based analysis report with the following structure:
            - Title of the report
            - Introduction
            - Bullet points listing 5-10 new AI projects and tools
              - Each bullet point must include:
                - The name of the AI company, product, or model
                - 3 sentences describing the project or tool
            - Conclusion
            The report should be detailed and concise, summarizing the most exciting new AI projects and tools found on the LocalLLama subreddit.
            """)
        )

    def task_blog(self):
        return Task(
            description=dedent("""
            Write a blog article with text only and with a short but impactful headline and at least 10 paragraphs. The blog should summarize the report on the latest AI tools found on the LocalLLama subreddit. The style and tone should be compelling and concise, fun, technical but also use layman words for the general public. Name specific new, exciting projects, apps, and companies in the AI world. Don't write "**Paragraph [number of the paragraph]:**", instead start the new paragraph in a new line. Write the names of projects and tools in BOLD. ALWAYS include links to the post page. ONLY include information from LocalLLAma.
            """),
            agent=CrewAgents().writer(),
            expected_output=dedent("""
            A text-only blog article with the following structure:
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
            ```
            """)
        )

    def task_critique(self):
        return Task(
            description=dedent("""
            The task entails summarizing and critiquing AI projects from the LocalLLama subreddit. The output must be formatted in Markdown and include interesting facts and personal thoughts on how each project connects to the overall theme of the newsletter.
            """),
            agent=CrewAgents().critic(),
            output_file='research_report.html',
            expected_output=dedent("""
            An HTML file named research_report.html containing the blog article.'
            """)
        )