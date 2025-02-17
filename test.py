import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
api_key = os.getenv('REDDIT_USERNAME')
# client_id = os.getenv('CLIENT_ID')
# secret_key = os.getenv('SECRET_KEY')

print(f"API Key: {api_key}")
# print(f"Client ID: {client_id}")
# print(f"Secret Key: {secret_key}")