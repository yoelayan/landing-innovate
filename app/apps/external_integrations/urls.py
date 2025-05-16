from django.urls import path
from . import views

app_name = 'external_integrations'

urlpatterns = [
    # OAuth flow URLs
    path('auth/gmail/', views.auth_gmail, name='auth_gmail'),
    path('auth/gmail/<int:auth_id>/', views.auth_gmail, name='auth_gmail_with_id'),
    path('callback/', views.oauth_callback, name='oauth_callback'),
    path('revoke/<int:auth_id>/', views.revoke_auth, name='revoke_auth'),
    path('test/<int:auth_id>/', views.test_connection, name='test_connection'),
]
