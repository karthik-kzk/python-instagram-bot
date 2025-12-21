import os
import requests
import subprocess


def videoDownloader(post):
    save_folder = "media/"

    # Ensure folder exists
    os.makedirs(save_folder, exist_ok=True)

    video_mp4 = post.get("video_mp4")      # video only
    dash_url = post.get("video_dash")      # video+audio manifest

    # REQUIRE BOTH VIDEO + DASH AUDIO
    if not video_mp4 or not dash_url:
        print("❌ Skipped — video or DASH missing:", post.get("title"))
        return

    # sanitize filename
    filename = "".join(x for x in post["title"]
                       if x.isalnum() or x in (" ", "_", "-"))
    
    post["filename"]=filename

    video_temp = f"{save_folder}/{filename}_video.mp4"
    audio_temp = f"{save_folder}/{filename}_audio.m4a"
    output_file = f"{save_folder}/{filename}.mp4"

    print(f"⬇️ Downloading → {output_file}")

    # -------------------------
    # 1️⃣ DOWNLOAD VIDEO TRACK
    # -------------------------
    print("📥 Downloading VIDEO track...")
    try:
        response = requests.get(video_mp4, stream=True)
        response.raise_for_status()
        with open(video_temp, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
    except Exception as e:
        print("❌ Video download failed:", e)
        return

    # -------------------------
    # 2️⃣ EXTRACT AUDIO TRACK
    # -------------------------
    print("🎵 Extracting AUDIO from DASH...")
    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", dash_url,
            "-vn", "-acodec", "copy",
            audio_temp
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("❌ Audio extract failed:", e)
        os.remove(video_temp)
        return

    # if audio missing → skip
    if not os.path.exists(audio_temp) or os.path.getsize(audio_temp) < 1000:
        print("❌ No audio track found → skipping")
        os.remove(video_temp)
        if os.path.exists(audio_temp):
            os.remove(audio_temp)
        return

    # -------------------------
    # 3️⃣ MERGE AUDIO + VIDEO
    # -------------------------
    print("🔗 Merging VIDEO + AUDIO...")
    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_temp,
            "-i", audio_temp,
            "-c:v", "copy",
            "-c:a", "aac",
            output_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("❌ Merge failed:", e)
        os.remove(video_temp)
        os.remove(audio_temp)
        return

    # -------------------------
    # 4️⃣ CLEAN TEMP FILES
    # -------------------------
    os.remove(video_temp)
    os.remove(audio_temp)

    print("✅ Download complete with audio:", output_file)




# import yt_dlp

# def videoDownloader(post):
#     # URL of the YouTube video and reddit videos
#     video_url = post["url"]
#     # video_url=post["url"]
#     save_folder = "media/" 
  

#     # Define download options
#     options = {
#         "user_agent": "Mozilla/5.0",
#         # "format": "mp4",  # Ensure MP4 format
#         "outtmpl": f"{save_folder}/{post["title"]}.%(ext)s",  # Save file with video title
#         # "outtmpl": f"{save_folder}/%(title)s.%(ext)s",  # Save file with video title
#     }

#     # Download the video
#     with yt_dlp.YoutubeDL(options) as ydl:
#         ydl.download([video_url])

#     print("Download complete!")

