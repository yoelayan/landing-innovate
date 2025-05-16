"""
Utility script to set up OAuth credentials for Google Gmail API.

This should be run as a standalone script to create the initial OAuth tokens:
python manage.py shell < apps/core/oauth_setup.py
"""

import os
import json
import sys
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def setup_oauth():
    """
    Set up OAuth credentials for Gmail API
    
    This script needs to be run once to generate the refresh token.
    """
    print("Starting OAuth setup...")
    
    # Define the scopes you need
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    # Check if we have credential info
    print(f"CLIENT_ID exists: {bool(settings.GOOGLE_MAIL_CLIENT_ID)}")
    print(f"CLIENT_SECRET exists: {bool(settings.GOOGLE_MAIL_CLIENT_SECRET)}")
    
    if not settings.GOOGLE_MAIL_CLIENT_ID or not settings.GOOGLE_MAIL_CLIENT_SECRET:
        print("Error: GOOGLE_MAIL_CLIENT_ID and GOOGLE_MAIL_CLIENT_SECRET must be set in .env")
        return
    
    # Some basic validation on client ID format
    if not settings.GOOGLE_MAIL_CLIENT_ID.endswith('apps.googleusercontent.com'):
        print(f"Warning: CLIENT_ID may be invalid: {settings.GOOGLE_MAIL_CLIENT_ID}")
    
    # Create the client config dictionary expected by InstalledAppFlow
    client_config = {
        "installed": {
            "client_id": settings.GOOGLE_MAIL_CLIENT_ID,
            "client_secret": settings.GOOGLE_MAIL_CLIENT_SECRET,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    print(f"Client config prepared: {json.dumps(client_config, indent=2)}")
    
    creds = None
    
    # Try to use saved credentials (if any)
    try:
        if settings.GOOGLE_MAIL_REFRESH_TOKEN:
            print(f"Found existing refresh token, attempting to use it...")
            creds = Credentials(
                token=None,
                refresh_token=settings.GOOGLE_MAIL_REFRESH_TOKEN,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=settings.GOOGLE_MAIL_CLIENT_ID,
                client_secret=settings.GOOGLE_MAIL_CLIENT_SECRET,
                scopes=SCOPES
            )
    except Exception as e:
        print(f"Could not load saved credentials: {e}")
    
    # If no valid credentials, go through authorization flow
    if not creds:
        print("No valid credentials found, starting new authorization flow...")
        try:
            flow = InstalledAppFlow.from_client_config(
                client_config, SCOPES)
            creds = flow.run_local_server(port=0)
            print("New credentials obtained successfully")
            
            # Display the refresh token that should be added to .env
            print("\n*** SAVE THIS REFRESH TOKEN IN YOUR .env FILE ***")
            print(f"GOOGLE_MAIL_REFRESH_TOKEN={creds.refresh_token}")
            print("****************************************\n")
        except Exception as e:
            print(f"Error during authorization flow: {e}")
            import traceback
            traceback.print_exc()
            return
    else:
        try:
            # If we have credentials but they're expired, refresh them
            if creds.expired and creds.refresh_token:
                print("Credentials expired, attempting to refresh...")
                creds.refresh(Request())
                print("Credentials refreshed successfully")
        except Exception as e:
            print(f"Error refreshing credentials: {e}")
            import traceback
            traceback.print_exc()
    
    # Test the credentials by making a simple API call
    try:
        print("Testing credentials with Gmail API...")
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        print(f"Successfully connected to Gmail API for: {profile['emailAddress']}")
        print("OAuth setup completed successfully!")
    except Exception as e:
        print(f"Error testing Gmail API connection: {e}")
        import traceback
        traceback.print_exc()

# Make sure this runs when the script is loaded in the Django shell
print("Setting up OAuth for Gmail API...")
setup_oauth()
print("OAuth setup script completed.") 