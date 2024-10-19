import os
import webbrowser
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_authenticated_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)

# ... (rest of the existing functions)

def main():
    # Load configuration
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    channel_name = config['channel_name']
    link_opener_active = config['link_opener_active']

    youtube = get_authenticated_service()
    
    channel_id = get_channel_id(youtube, channel_name)
    
    if not channel_id:
        print(f"Channel '{channel_name}' not found. Exiting.")
        return

    print(f"Monitoring live chat for channel: {channel_name}")
    if link_opener_active:
        print("The script is now running. It will automatically open links posted by the creator.")
    else:
        print("The script is now running. It will display links posted by the creator.")
    print("Press Ctrl+C to stop the script.")
    
    while True:
        try:
            video_id = get_live_video_id(youtube, channel_id)
            
            if not video_id:
                print("No live stream found. Checking again in 60 seconds...")
                time.sleep(60)
                continue

            live_chat_id = get_live_chat_id(youtube, video_id)
            
            if not live_chat_id:
                print("Live chat not available. Checking again in 60 seconds...")
                time.sleep(60)
                continue

            print(f"Live stream found. Monitoring chat for creator links...")
            
            next_page_token = None
            
            while True:
                chat_response = get_chat_messages(youtube, live_chat_id, next_page_token)
                
                if link_opener_active:
                    open_creator_links(chat_response['items'], channel_id)
                else:
                    display_creator_links(chat_response['items'], channel_id)
                
                next_page_token = chat_response.get('nextPageToken')
                polling_interval = chat_response['pollingIntervalMillis'] / 1000
                
                time.sleep(polling_interval)

        except KeyboardInterrupt:
            print("\nScript stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Restarting in 60 seconds...")
            time.sleep(60)

def display_creator_links(messages, creator_channel_id):
    for message in messages:
        if message['authorDetails']['channelId'] == creator_channel_id:
            message_text = message['snippet']['displayMessage']
            if 'http://' in message_text or 'https://' in message_text:
                links = [word for word in message_text.split() if word.startswith(('http://', 'https://'))]
                for link in links:
                    print(f"Creator posted a link: {link}")

if __name__ == "__main__":
    main()
