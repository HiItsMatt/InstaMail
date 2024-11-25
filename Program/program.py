import os
import time
import openai
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build

# Define the scope for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


#Retrieve the last processed email ID from a file.
def get_last_email_id():

    try:
        with open('last_email_id.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None  # No file exists yet

#Save the last processed email ID to a file.
def save_last_email_id(email_id):
    with open('last_email_id.txt', 'w') as file:
        file.write(email_id)

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

#find 10 most recent emails, check if each email is new, and list new ones.
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
        
        # Extract the email content
        body = get_email_body(payload)
        if body:
            print("Summarizing email...")
            summary = summarize_email(body)
            print(f"Summary: {summary}")
        else:
            print(f"Could not extract body from email ID {msg_id}")

        # Update the newest_email_id
        if not newest_email_id:
            newest_email_id = msg_id

    # Save the ID of the newest email after processing all new messages
    if newest_email_id:
        save_last_email_id(newest_email_id)

#Extract the body content from an email's payload.
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

#Load the OpenAI API key from a file.
def load_api_key():
    try:
        with open('openai_api_key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: API key file not found. Make sure 'openai_api_key.txt' exists.")
        exit()

#Query OpenAI to summarize the email content.
def summarize_email(content):
    try:
        openai.api_key = load_api_key()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the correct model
            messages=[
                {"role": "system", "content": "You are an assistant that reads my emails and sends me text message summaries. you speak casually, as though we are close friends"},
                {"role": "user", "content": f"Email: {content}"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        # Extract the summary from the response
        summary = response['choices'][0]['message']['content']
        return summary.strip()
    except Exception as e:
        print(f"Error querying OpenAI: {e}")
        return "Error generating summary."
    
def sleepLoop(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)  # Convert seconds to minutes and seconds
        time.sleep(1)  # Wait for 1 second
        seconds -= 1

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def displaySplash():
    clear_terminal()
    print(r"""
              _       ______  __       ____    ___   ______ 
|\    /|     / \     |__  __| ||      | __ \  / _ \ |__  __|
| \  /||    / _ \       ||    ||      ||__|/  || ||    ||   
||\\//||   / /_\ \      ||    ||      | __ \  || ||    ||   
|| \/ ||  / _____ \   __||__  ||____  ||__| | ||_||    ||   
||    || /_/     \_\ |______| |_____| |____/  \___/    ||   
 __________________________________________________________ 
|\___..................................................___/|
|####\___..........................................___/####|
|########\___..................................___/########|
|############\___..........................___/############|
|################\___..................___/################|
|####################\___..........___/####################|
|########################\___..___/########################|
|############################\/############################|
|##########################################################|
|##########################################################|
|##########################################################|
|##########################################################|
|##########################################################|
|##########################################################|
|##########################################################|
|##########################################################|
""")
    
    time.sleep(1)
    print(r"""
 __________________________________________________________ 
|---> Created By:  Matthew Shanahan                        |
|---> Contact Me:                                          |
|     -->  Insta:    _hi_its_matt                          |
|     -->  Discord:   hi_its_matt                          |
|__________________________________________________________|
""")                                                            



#check for new emails every 60s
if __name__ == '__main__':
    displaySplash()
    while True:
        list_new_emails()
        sleepLoop(60)