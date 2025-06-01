from instagrapi import Client
from createFolder import createFolder
from delete_folder_contents import delete_folder_contents
from ffmpegVersionCheck import ffmpeg_version_match
from is_internet_available import is_internet_available
from last_run import last_run_today, update_last_run
from logger import logError
from login import login_user
from redditScraper import redditScraper
from videoDownloader import videoDownloader
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()


# requires python 3.13.2 !important

if not is_internet_available():
    logError("internet not working")
    sys.exit()

if last_run_today():
    print("already run today")
    logError("already run today")
    sys.exit()
    
if not ffmpeg_version_match():
    print("ffmpeg version version mismatch")
    logError("ffmpeg version version mismatch")
    sys.exit()

# sys.exit()

folder_path = "media/"
createFolder(folder_path)
delete_folder_contents(folder_path)

no_of_accounts = [1,2,3,4]
for val in no_of_accounts:
    INSTAGRAM_USERNAME = os.getenv(f'INSTAGRAM_USERNAME_{val}')
    INSTAGRAM_PASSWORD = os.getenv(f'INSTAGRAM_PASSWORD_{val}')
    subreddit_name = os.getenv(f'SUBREDDIT_NAME_{val}')
    session_file=f"session{val}.json"
    
    time_filter = "day"  # Options: "hour", "day", "week", "month", "year", "all"
    outputArrayLimit = 10
    fetchPostLimit = 10
    try:
       topPost = redditScraper(time_filter, outputArrayLimit,
                            fetchPostLimit, subreddit_name)
    except Exception as e:
        logError(e)
        continue
    # sys.exit()
    for index, post in enumerate(topPost, start=1):
        try:
            videoDownloader(post)        
        except Exception as e:
            logError(e)
        print(f"Downloaded {index} / {len(topPost)}")
        

    # sys.exit()
    # login instagram user
    try:
        cl = login_user(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, session_file)
    except Exception as e:
        logError(e)
        continue

    for index, post in enumerate(topPost, start=1):
        try:
            cl.clip_upload(
                f"media/{post["title"]}.mp4",
                f"{post["title"]}"
            )        
        except Exception as e:
            logError(e)
        print(f"Uploaded {index} / {len(topPost)}")

    

update_last_run()
