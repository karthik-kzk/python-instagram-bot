from instagrapi import Client
from createFolder import createFolder
from delete_folder_contents import delete_folder_contents
from last_run import  last_run_today, update_last_run
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
outputArrayLimit=5
fetchPostLimit=5
topPost=redditScraper(time_filter,outputArrayLimit,fetchPostLimit)
# print(topPost)
for index, post in enumerate(topPost, start=1):
    videoDownloader(post) 
    print(f"Download {index} / {len(topPost)}")   

# sys.exit()
cl = Client()

INSTAGRAM_USERNAME=os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD=os.getenv('INSTAGRAM_PASSWORD')
cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


for index, post in enumerate(topPost, start=1):
    cl.clip_upload(
    f"media/{post["title"]}.mp4",    
    f"{post["title"]}"    
)
    print(f"Upload {index} / {len(topPost)}")
    
update_last_run()

   