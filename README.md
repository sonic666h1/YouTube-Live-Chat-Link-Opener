# YouTube Live Chat Link Opener

This script monitors a specified YouTube channel's live chat and opens (or displays) links posted by the channel creator.

## Setup Instructions

1. Install Python 3.7 or higher if you haven't already.

2. Install the required libraries:
   ```
   pip install google-auth-oauthlib google-api-python-client
   ```

3. Set up a Google Cloud project and enable the YouTube Data API v3:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3 for your project
   - Create OAuth 2.0 Client ID credentials (Desktop app)
   - Download the client configuration and save it as `client_secret.json` in the same directory as the script

4. Edit the `config.json` file to set your preferred channel name and whether you want links to be opened automatically:
   ```json
   {
     "channel_name": "YourPreferredChannel",
     "link_opener_active": true
   }
   ```

5. Run the script:
   ```
   python op.py
   ```

6. The first time you run the script, it will open a browser window for you to authenticate with your Google account. Grant the necessary permissions.

7. The script will now monitor the specified channel's live chat for links posted by the creator.

## Notes

- If `link_opener_active` is set to `true` in `config.json`, the script will automatically open links in your default web browser.
- If `link_opener_active` is set to `false`, the script will only display the links in the console.
- You can stop the script at any time by pressing Ctrl+C.

## Security

- Keep your `client_secret.json` and `token.json` files secure and do not share them with others.
- Each user should set up their own Google Cloud project and credentials for security reasons.

## why?

- Can be used to open roblox games immediatly to get in a giveaway server or game that you want to join in with your favorite creator.
