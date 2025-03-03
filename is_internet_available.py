# test code

import socket


def is_internet_available():
    try:
        # Try connecting to a public DNS server (Google)
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


# Check internet
if is_internet_available():
    print("✅ Internet is working!")
else:
    print("❌ No internet connection.")
