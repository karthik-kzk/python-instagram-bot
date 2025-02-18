from instagrapi import Client
from createFolder import createFolder
from delete_folder_contents import delete_folder_contents
from last_run import last_run_today, update_last_run
from logger import logError
from redditScraper import redditScraper
from videoDownloader import videoDownloader
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()

if last_run_today():
    print("already run today")
    sys.exit()

# sys.exit()

folder_path = "media/"
createFolder(folder_path)
delete_folder_contents(folder_path)


time_filter = "day"  # Options: "hour", "day", "week", "month", "year", "all"
outputArrayLimit = 10
fetchPostLimit = 10
topPost = redditScraper(time_filter, outputArrayLimit, fetchPostLimit)
# sys.exit()
for index, post in enumerate(topPost, start=1):
    try:
        videoDownloader(post)
        print(f"Downloaded {index} / {len(topPost)}")
    except Exception as e:
        logError(e)    
    

# sys.exit()
cl = Client()

INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


for index, post in enumerate(topPost, start=1):
    try:
        cl.clip_upload(
            f"media/{post["title"]}.mp4",
            f"{post["title"]}"
        )
        print(f"Uploaded {index} / {len(topPost)}")
    except Exception as e:
        logError(e)

    

update_last_run()
