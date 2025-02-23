# test code

from logger import logError
from login import login_user
import os
import sys

print(os.path.exists("session1.json"))

cl = login_user()

try:
   cl.clip_upload(
    f"media/test 😂🤍.mp4",
    f"test 😂🤍"
)
except Exception as e:
    logError(e)
