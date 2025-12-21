import praw
import os
import json
import requests
from dotenv import load_dotenv


# ----------------------------
# LOAD ENVIRONMENT VARIABLES
# ----------------------------
load_dotenv()

client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = "python:reddit.video.scraper:v1.0 (by u/yourname)"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)


# ----------------------------
# VIDEO URL EXTRACTOR
# ----------------------------
def extract_video_urls(post):
    """
    Extracts video URLs from Reddit post object.
    Returns (video_mp4, video_dash) tuple or (None, None)
    """

    video_mp4 = None
    video_dash = None

    # Case 1: media.reddit_video
    if post.media and post.media.get("reddit_video"):
        video_mp4 = post.media["reddit_video"].get("fallback_url")
        video_dash = post.media["reddit_video"].get("dash_url")

    # Case 2: secure_media.reddit_video
    elif post.secure_media and post.secure_media.get("reddit_video"):
        video_mp4 = post.secure_media["reddit_video"].get("fallback_url")
        video_dash = post.secure_media["reddit_video"].get("dash_url")

    # Case 3: preview.reddit_video_preview
    elif hasattr(post, "preview") and post.preview.get("reddit_video_preview"):
        video_mp4 = post.preview["reddit_video_preview"].get("fallback_url")
        video_dash = post.preview["reddit_video_preview"].get("dash_url")

    # Case 4: crosspost parent
    elif hasattr(post, "crosspost_parent_list"):
        cp = post.crosspost_parent_list[0]
        if "media" in cp and cp["media"].get("reddit_video"):
            video_mp4 = cp["media"]["reddit_video"].get("fallback_url")
            video_dash = cp["media"]["reddit_video"].get("dash_url")

    return video_mp4, video_dash


# ----------------------------
# DASH URL VALIDATION
# ----------------------------
def verify_dash(url):
    try:
        r = requests.head(url)
        return r.status_code == 200
    except:
        return False


# ----------------------------
# MAIN SCRAPER FUNCTION
# ----------------------------
def redditScraper(time_filter, output_limit, fetch_limit, subreddit_name):
    
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = []

    for post in subreddit.top(time_filter, limit=fetch_limit):

        # NSFW filter + ensure video
        if not post.over_18 and post.is_video and len(top_posts) < output_limit:

            video_mp4, video_dash = extract_video_urls(post)

            # 🔥 REQUIRE DASH VIDEO & AUDIO
            if not video_dash or not verify_dash(video_dash):
                continue

            post_data = {
                "title": post.title,
                "url": post.url,
                "video_mp4": video_mp4,
                "video_dash": video_dash,
                "score": post.score,
                "author": str(post.author),
                "created_utc": post.created_utc,
                "comments": post.num_comments
            }

            top_posts.append(post_data)

    print("DASH videos found:", len(top_posts), "/", fetch_limit)

    # finish if enough posts OR too many fetch loops
    if len(top_posts) >= output_limit or fetch_limit > 30:

        with open("top_posts_reddit.json", "w", encoding="utf-8") as json_file:
            json.dump(top_posts, json_file, indent=4)

        print("Saved DASH posts → top_posts_reddit.json")
        return top_posts

    return redditScraper(time_filter, output_limit, fetch_limit + 1, subreddit_name)



 # Save to JSON file
# with open(f"top_posts_reddit.json", "w", encoding="utf-8") as json_file:
#     json.dump(top_posts, json_file, indent=4)

# print("Top posts saved to JSON file!")
