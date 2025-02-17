import yt_dlp

def videoDownloader(post):
    # URL of the YouTube video and reddit videos
    video_url = post["url"]
    # video_url=post["url"]
    save_folder = "media/" 
  

    # Define download options
    options = {
        # "format": "mp4",  # Ensure MP4 format
        "outtmpl": f"{save_folder}/{post["title"]}.%(ext)s",  # Save file with video title
        # "outtmpl": f"{save_folder}/%(title)s.%(ext)s",  # Save file with video title
    }

    # Download the video
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    print("Download complete!")

