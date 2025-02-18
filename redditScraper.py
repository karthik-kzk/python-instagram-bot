import praw
import datetime
import os
import json
from dotenv import load_dotenv

from checkDuplicate import isTitleDuplicate
# Load environment variables from the .env file
load_dotenv()

# Open the JSON file
# with open('top_posts_reddit.json', 'r') as file:
#     data = json.load(file)

# Set up Reddit API client
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')


user_agent = "python"

# Initialize Reddit API client
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Define the subreddit and time filter (top posts in the last day)
subreddit_name = os.getenv('SUBREDDIT_NAME')
time_filter = "day"  # Options: "hour", "day", "week", "month", "year", "all"
limit = 5

# Fetch the top posts in the last day, exclude adult content
subreddit = reddit.subreddit(subreddit_name)

# Loop through the top posts
top_posts = subreddit.top(time_filter=time_filter, limit=limit)

# Define a list to store non-adult content posts


def redditScraper(time_filter, outputArrayLimit, fetchPostLimit):
    top_posts = []
    for post in subreddit.top(time_filter, limit=fetchPostLimit):
        # Exclude adult content
        if not post.over_18 and len(top_posts) < outputArrayLimit and post.is_video:
            post_data = {
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "author": str(post.author),
                "created_utc": post.created_utc,
                "comments": post.num_comments
            }
            top_posts.append(post_data)

    print("topPost", len(top_posts), fetchPostLimit)
    if len(top_posts) == outputArrayLimit or fetchPostLimit>30:

        with open(f"top_posts_reddit.json", "w", encoding="utf-8") as json_file:
            json.dump(top_posts, json_file, indent=4)
        print("Top posts saved to JSON file!")
        return top_posts
    return redditScraper(time_filter, outputArrayLimit, fetchPostLimit+1)

 # Save to JSON file
# with open(f"top_posts_reddit.json", "w", encoding="utf-8") as json_file:
#     json.dump(top_posts, json_file, indent=4)

# print("Top posts saved to JSON file!")
