import subprocess
import re

def get_ffmpeg_version():
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # print(result)
        s = result.stdout.splitlines()[0]
        version_line = re.findall(r'\d+\.\d+', s)
        return version_line
    except FileNotFoundError:
        return "FFmpeg is not installed or not in the system PATH."


def ffmpeg_version_match():
    return get_ffmpeg_version()[0] == '7.1'


