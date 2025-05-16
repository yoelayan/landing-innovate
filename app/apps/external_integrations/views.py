from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect

import os
import json
import pickle
import datetime
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import GoogleAPIAuth

# Scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

@staff_member_required
def auth_gmail(request, auth_id=None):
    """Start the OAuth flow for Gmail API."""
    # Get the auth object or create a new one
    if auth_id:
        auth_obj = get_object_or_404(GoogleAPIAuth, id=auth_id)
    else:
        # Use the first auth object or redirect to the add page if none exists
        auth_obj = GoogleAPIAuth.objects.first()
        if not auth_obj:
            messages.error(request, "Please create a Google API authentication configuration first.")
            return redirect('admin:external_integrations_googleapiauth_add')
    
    # Create the flow using the client secrets
    client_config = {
        'web': {
            'client_id': auth_obj.client_id,
            'client_secret': auth_obj.client_secret,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [request.build_absolute_uri(reverse('external_integrations:oauth_callback'))]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=request.build_absolute_uri(reverse('external_integrations:oauth_callback'))
    )
    
    # Save the auth_id in the session for the callback
    request.session['auth_id'] = auth_obj.id
    
    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'  # Force to show the consent screen to get refresh_token
    )
    
    # Save the state for CSRF protection
    request.session['state'] = state
    
    # Redirect to the authorization URL
    return redirect(authorization_url)

@staff_member_required
def oauth_callback(request):
    """Handle the OAuth callback from Google."""
    # Get the state from the session
    state = request.session.get('state')
    auth_id = request.session.get('auth_id')
    
    if not state or not auth_id:
        messages.error(request, 'Error: Invalid session state.')
        return redirect('admin:external_integrations_googleapiauth_changelist')
    
    auth_obj = get_object_or_404(GoogleAPIAuth, id=auth_id)
    
    # Create the flow using the client secrets
    client_config = {
        'web': {
            'client_id': auth_obj.client_id,
            'client_secret': auth_obj.client_secret,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [request.build_absolute_uri(reverse('external_integrations:oauth_callback'))]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        state=state,
        redirect_uri=request.build_absolute_uri(reverse('external_integrations:oauth_callback'))
    )
    
    # Exchange the authorization code for a token
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    # Get the credentials and store them
    credentials = flow.credentials
    
    # Update the auth object
    auth_obj.access_token = credentials.token
    auth_obj.refresh_token = credentials.refresh_token
    
    if credentials.expiry:
        auth_obj.token_expiry = credentials.expiry
    
    auth_obj.authorized = True
    auth_obj.save()
    
    # Update settings refresh token
    # Note: This is a workaround, in production you might want to use environment variables or settings overrides
    
    messages.success(request, 'Successfully authenticated with Google Gmail API!')
    return redirect('admin:external_integrations_googleapiauth_change', object_id=auth_obj.id)

@staff_member_required
def revoke_auth(request, auth_id):
    """Revoke the OAuth authorization."""
    auth_obj = get_object_or_404(GoogleAPIAuth, id=auth_id)
    
    # Create credentials object
    creds = Credentials(
        token=auth_obj.access_token,
        refresh_token=auth_obj.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=auth_obj.client_id,
        client_secret=auth_obj.client_secret
    )
    
    try:
        # Revoke the token
        if creds.valid:
            Request().post(
                'https://oauth2.googleapis.com/revoke',
                params={'token': creds.token},
                headers={'content-type': 'application/x-www-form-urlencoded'}
            )
    except Exception as e:
        messages.warning(request, f'Error revoking token: {e}')
    
    # Update the auth object
    auth_obj.access_token = None
    auth_obj.refresh_token = None
    auth_obj.token_expiry = None
    auth_obj.authorized = False
    auth_obj.save()
    
    messages.success(request, 'Authorization revoked successfully.')
    return redirect('admin:external_integrations_googleapiauth_changelist')

@staff_member_required
def test_connection(request, auth_id):
    """Test the Gmail API connection."""
    auth_obj = get_object_or_404(GoogleAPIAuth, id=auth_id)
    
    if not auth_obj.is_active():
        messages.error(request, 'The connection is not active. Please authenticate first.')
        return redirect('admin:external_integrations_googleapiauth_change', object_id=auth_obj.id)
    
    # Create credentials object
    creds = Credentials(
        token=auth_obj.access_token,
        refresh_token=auth_obj.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=auth_obj.client_id,
        client_secret=auth_obj.client_secret
    )
    
    # Refresh the token if it's expired
    if creds.expired:
        try:
            creds.refresh(Request())
            auth_obj.access_token = creds.token
            if creds.expiry:
                auth_obj.token_expiry = creds.expiry
            auth_obj.save()
        except Exception as e:
            messages.error(request, f'Error refreshing token: {e}')
            return redirect('admin:external_integrations_googleapiauth_change', object_id=auth_obj.id)
    
    # Test the connection by getting the user profile
    try:
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        
        # Update the last used timestamp
        auth_obj.use_token()
        
        messages.success(request, f'Connection successful! Email address: {profile.get("emailAddress")}')
    except HttpError as error:
        messages.error(request, f'Error testing connection: {error}')
    
    return redirect('admin:external_integrations_googleapiauth_change', object_id=auth_obj.id)
