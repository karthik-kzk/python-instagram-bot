from datetime import datetime
import json

tracker_file_path = 'session/tracker.json'
# Open the JSON file
with open(tracker_file_path, 'r') as file:
    data = json.load(file)

def last_run_today():
    today_date = datetime.today().date().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime("%I:%M:%S %p")
    data["last_run_time"]=current_time
    with open(tracker_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    if today_date==data["last_run"]:
        return True
    return False

def update_last_run():
    today_date = datetime.today().date().strftime('%Y-%m-%d')
    data["last_run"]=today_date
    with open(tracker_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print("JSON file has been updated.")



