# test code

from logger import logError
from login import login_user
import os
import sys
name = "session1.json"
print(os.path.exists(f"session/{name}"))
name = "test"
string = f"My name is {name} and I am age years old."
print(string)

# cl = login_user()


# try:
#    cl.clip_upload(
#     f"media/test 😂🤍.mp4",
#     f"test 😂🤍"
# )
# except Exception as e:
#     logError(e)
