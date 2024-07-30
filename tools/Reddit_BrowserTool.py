class Reddit_BrowserTool:
    @tool("Scrape reddit content")
    def scrape_reddit(max_comments_per_post=7):
        """Useful to scrape a reddit content"""
        reddit = praw.Reddit(
            client_id="hrwfUNc2xubrhwrlHDStNA",
            client_secret="QzqidqUIkYuwN3g4MoNlm2rLARgw_A",
            user_agent="user-agent",
        )
        subreddit = reddit.subreddit("LocalLLaMA")
        scraped_data = []

        for post in subreddit.hot(limit=12):
            post_data = {"title": post.title, "url": post.url, "comments": []}

            try:
                post.comments.replace_more(limit=0)  # Load top-level comments only
                comments = post.comments.list()
                if max_comments_per_post is not None:
                    comments = comments[:7]

                for comment in comments:
                    post_data["comments"].append(comment.body)

                scraped_data.append(post_data)

            except praw.exceptions.APIException as e:
                print(f"API Exception: {e}")
                time.sleep(60)  # Sleep for 1 minute before retrying

        return scraped_data
