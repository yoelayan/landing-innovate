import os
import json
import pickle
from django.core.management.base import BaseCommand
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings
import environ

class Command(BaseCommand):
    help = 'Get OAuth2 tokens for Gmail API'

    def add_arguments(self, parser):
        parser.add_argument('--client-id', type=str, help='OAuth client ID (optional if in .env)')
        parser.add_argument('--client-secret', type=str, help='OAuth client secret (optional if in .env)')
        parser.add_argument('--save', action='store_true', help='Save credentials to .env file')

    def handle(self, *args, **options):
        # Load .env file
        env_path = os.path.join(settings.BASE_DIR.parent, '.env')
        if os.path.exists(env_path):
            env = environ.Env()
            environ.Env.read_env(env_path)
        
        client_id = options.get('client_id') or os.environ.get('GOOGLE_MAIL_CLIENT_ID')
        client_secret = options.get('client_secret') or os.environ.get('GOOGLE_MAIL_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR('Client ID and Client Secret are required!'))
            self.stdout.write(self.style.WARNING('Add them to your .env file as GOOGLE_MAIL_CLIENT_ID and GOOGLE_MAIL_CLIENT_SECRET'))
            self.stdout.write(self.style.WARNING('Or run with: python manage.py get_gmail_oauth_token --client-id=ID --client-secret=SECRET'))
            return

        # Define the scopes for Gmail
        SCOPES = ['https://mail.google.com/']
        
        creds = None
        token_file = os.path.join(settings.BASE_DIR, 'gmail_token.pickle')
        
        # Check if we have token stored already
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no valid credentials, let's get some
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Create a flow with our client info
                client_config = {
                    "installed": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                    }
                }
                
                flow = InstalledAppFlow.from_client_config(
                    client_config, SCOPES)
                
                self.stdout.write(self.style.SUCCESS('Starting OAuth flow...'))
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Display token details
        self.stdout.write(self.style.SUCCESS('Authentication successful!'))
        self.stdout.write('Access Token: ' + creds.token)
        self.stdout.write('Refresh Token: ' + creds.refresh_token)
        self.stdout.write('Token Expiry: ' + str(creds.expiry))
        
        # If save flag is provided, try to update .env file
        if options.get('save'):
            try:
                env_path = os.path.join(settings.BASE_DIR.parent, '.env')
                if os.path.exists(env_path):
                    with open(env_path, 'r') as file:
                        lines = file.readlines()
                    
                    with open(env_path, 'w') as file:
                        for line in lines:
                            if line.startswith('GOOGLE_MAIL_REFRESH_TOKEN='):
                                file.write(f'GOOGLE_MAIL_REFRESH_TOKEN="{creds.refresh_token}"\n')
                            else:
                                file.write(line)
                    
                    self.stdout.write(self.style.SUCCESS('Updated .env file with refresh token'))
                else:
                    self.stdout.write(self.style.ERROR('.env file not found'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to update .env file: {e}'))
                
        self.stdout.write(self.style.SUCCESS('\nAdd these tokens to your .env file:'))
        self.stdout.write('GOOGLE_MAIL_REFRESH_TOKEN="' + creds.refresh_token + '"') 