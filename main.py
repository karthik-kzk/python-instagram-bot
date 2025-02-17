from instagrapi import Client
from redditScraper import redditScraper
from videoDownloader import videoDownloader
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()

time_filter = "day"  # Options: "hour", "day", "week", "month", "year", "all"
outputArrayLimit=5
fetchPostLimit=5
topPost=redditScraper(time_filter,outputArrayLimit,fetchPostLimit)
# print(topPost)
for post in topPost:
    videoDownloader(post)    

# sys.exit()
cl = Client()

INSTAGRAM_USERNAME=os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD=os.getenv('INSTAGRAM_PASSWORD')
cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

# user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
for post in topPost:
    media = cl.clip_upload(
    f"media/{post["title"]}.mp4",    
    f"{post["title"]}"    
)

    media.dict()