import os
import shutil

def delete_folder_contents(folder_path):
    # Loop through the contents of the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file or directory
        if os.path.isfile(file_path):
            os.remove(file_path)  # Delete the file
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Delete the directory and its contents

folder_path = "media/"
delete_folder_contents(folder_path)
print("Folder contents deleted.")