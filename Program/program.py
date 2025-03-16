# -----------------------------------
# Group 0: Import Libraries
# -----------------------------------

import os
import time
import openai
import base64

from pystray import Icon, MenuItem, Menu
from PIL import Image
import sys
import threading

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from instagrapi import Client

from dotenv import load_dotenv

load_dotenv()

# -----------------------------------
# Group 1: System Tray Functions
# -----------------------------------

def run_program():
    displaySplash()
    # Your existing main logic here
    while True:
        list_new_emails()
        sleepLoop(5)

def create_image():
    # Load your PNG file
    icon_path = "icon.png"  # Replace with the actual path to your PNG
    return Image.open(icon_path)

def on_quit(icon, item):
    # Cleanup and exit when quitting
    icon.stop()
    sys.exit()

def setup_tray():
    # Define the tray menu
    menu = Menu(
        MenuItem("Quit", on_quit)
    )
    icon = Icon("EmailBot", create_image(), "InstaMail", menu)
    icon.run()

# -----------------------------------
# Group 2: Instagrapi Functions
# -----------------------------------

def send_insta_message(message):
    try:
        # Initialize the client
        cl = Client()

        # Log in to Instagram
        print("Logging into Instagram...")
        cl.login(os.getenv("INSTA_USERNAME"), os.getenv("INSTA_PASSWORD"))
        print("Login successful!")

        # Define recipient and message
        recipient_username = "_hi_its_matt"  # Replace with the actual username

        # Fetch the user ID from the username
        user_id = cl.user_id_from_username(recipient_username)

        # Send the message
        cl.direct_send(message, [user_id])

        print(f"Sent: {message} to {recipient_username}")

    except Exception as e:
        print(f"Error sending Instagram message: {e}")

# -----------------------------------
# Group 3: Gmail API Functions
# -----------------------------------

# Define the scope for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Extract the body content from an email's payload.
def get_email_body(payload):
    body = None

    # Look for plain text content
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':  # Prefer plain text
                body = part['body'].get('data')
                break
            elif part['mimeType'] == 'text/html':  # Fallback to HTML
                body = part['body'].get('data')
    else:
        # If no parts, try the main body
        body = payload.get('body', {}).get('data')
    if body:
        # Decode the content from base64
        body_decoded = base64.urlsafe_b64decode(body).decode('utf-8')
        return body_decoded.strip()
    return None

# Find 10 most recent emails, check if each email is new, and send new ones to me on instagram
def list_new_emails():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Get the last processed email ID
    last_email_id = get_last_email_id()

    # Fetch emails
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No messages found.")
        return

    print("Checking for new messages...")
    newest_email_id = None  # Track the ID of the newest email

    for msg in messages:
        msg_id = msg['id']

        # Stop processing if we've already seen this email
        if msg_id == last_email_id:
            print("No new messages.")
            break

        # Fetch the full email
        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = message.get('payload', {})
        
        # Extract the email content and print
        body = get_email_body(payload)
        if body:
            print("Summarizing email...")
            summary = summarize_email(body)
            print("")
            send_insta_message(summary)
        else:
            print(f"Could not extract body from email ID {msg_id}")

        # Update the newest_email_id
        if not newest_email_id:
            newest_email_id = msg_id

    # Save the ID of the newest email after processing all new messages
    if newest_email_id:
        save_last_email_id(newest_email_id)

# Retrieve the last processed email ID from a file.
def get_last_email_id():
    try:
        with open('last_email_id.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None  # No file exists yet

# Save the last processed email ID to a file.
def save_last_email_id(email_id):
    with open('last_email_id.txt', 'w') as file:
        file.write(email_id)

# Authenticate with Gmail to get access token to gmail account
def authenticate_gmail():
    creds = None

    # Check if token.json exists (this saves your session)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no valid credentials, go through the login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# -----------------------------------
# Group 4: OpenAI API Functions
# -----------------------------------

# Load the OpenAI API key from a file.
def load_api_key():
    try:
        with open('openai_api_key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: API key file not found. Make sure 'openai_api_key.txt' exists.")
        exit()

# Query OpenAI to summarize the email content.
def summarize_email(content):
    try:
        client = openai.OpenAI()  # Create an OpenAI client
        response = client.chat.completions.create(
            model="gpt-4",  # Use the correct model
            messages=[
                {"role": "system", "content": "The prompts you receive are emails from other people. You should reply to me with the subject of the email and dot points summarizing what is discussed. At the end, state who the email was from as though you are the sender. You are my friendly personal assistant."},
                {"role": "user", "content": content}
            ],
            max_tokens=100,
            temperature=0.7
        )
        # Extract the summary from the response
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        print(f"Error querying OpenAI: {e}")
        return "Error generating summary."

# -----------------------------------
# Group 5: Utility Functions
# -----------------------------------

#wait a given amount of seconds before continuing
def sleepLoop(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)  # Convert seconds to minutes and seconds
        time.sleep(1)  # Wait for 1 second
        seconds -= 1

#clear the terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def displaySplash():
    print(r"""
 ________________________________________________________
|\______                                          ______/|
|%%%%%%%\______                            ______/%%%%%%%|
|%%%%%%%%%%%%%%\______              ______/%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%\_____  _____/%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%\/%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
""")
    time.sleep(0.5)
    print(r"""
 _________   __     _   _______   _________   ___
|___   ___| |  \   | | /  ____/  |___   ___| |   \
    | |     |   \  | | | /____       | |     | |\ \
    | |     | |\ \ | | \_____ \      | |     | |_\ \
    | |     | | \ \| | __    \ \     | |     | ____ \
 ___| |___  | |  \   | \ \___/ /     | |     | |   \ \
|_________| |_|   \__|  \_____/      |_|     |_|    \_\

 __    __   ___        _________   _
|  \  /  | |   \      |___   ___| | |
|   \/   | | |\ \         | |     | |
| |\  /| | | |_\ \        | |     | |
| | \/ | | | ____ \       | |     | |
| |    | | | |   \ \   ___| |___  | |_____
|_|    |_| |_|    \_\ |_________| |_______|
""")
    time.sleep(0.5)
    print(r"""--------------------------------------------------------

Created By Matthew Shanahan

--------------------------------------------------------
""")
    time.sleep(0.5)
    print(r"""Contact Me
    Instagram:  _hi_its_matt
    Discord:    hi_its_matt
    Email:      hi.its.ma77@gmail.com
""")

# -----------------------------------
# Group 6: Main Method
# -----------------------------------

if __name__ == "__main__":

    # Run the main program in a thread
    program_thread = threading.Thread(target=run_program, daemon=True)
    program_thread.start()

    # Setup the system tray
    setup_tray()