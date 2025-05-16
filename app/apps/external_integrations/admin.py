from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils import timezone
from .models import Integration, GoogleAPIAuth


# Integracion con admin
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("name", "ubication", "code_preview")
    search_fields = ("name", "ubication", "code")
    list_filter = ("ubication",)
    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "name",
                    "ubication",
                )
            },
        ),
        (
            "Código de Integración",
            {
                "fields": ("code",),
                "description": "Ingrese el código HTML o JavaScript que desea integrar en el sitio web.",
            },
        ),
    )

    def code_preview(self, obj):
        """
        Displays a preview of the code in the admin list view.
        """
        if obj.code:
            # Limit the preview to a certain number of characters
            return obj.code
        return "No code"

    code_preview.short_description = "Vista Previa del Código"


class GoogleAPIAuthAdmin(admin.ModelAdmin):
    list_display = ('name', 'authorized', 'last_used', 'auth_status', 'auth_actions')
    readonly_fields = ('created_at', 'updated_at', 'last_used', 'token_expiry', 'auth_status', 'auth_actions')
    list_filter = ('authorized',)
    search_fields = ('name',)
    fieldsets = (
        (
            "API Configuration",
            {
                "fields": (
                    "name",
                    "client_id",
                    "client_secret",
                ),
                "description": "Enter the Google API credentials from your Google Cloud Console.",
            },
        ),
        (
            "Authentication Status",
            {
                "fields": (
                    "authorized",
                    "auth_status",
                    "token_expiry",
                    "last_used",
                    "created_at",
                    "updated_at",
                ),
                "description": "Authentication status details.",
            },
        ),
        (
            "Authentication Actions",
            {
                "fields": ("auth_actions",),
                "description": "Actions for managing the authentication.",
            },
        ),
    )

    def auth_status(self, obj):
        """Display the authentication status with descriptive message."""
        if not obj.authorized:
            return format_html('<span style="color: red;">Not authenticated</span>')
        
        if not obj.refresh_token:
            return format_html('<span style="color: orange;">Missing refresh token</span>')
        
        if obj.token_expiry and obj.token_expiry < timezone.now():
            return format_html('<span style="color: orange;">Access token expired (will auto-refresh)</span>')
        
        return format_html('<span style="color: green;">Authenticated and active</span>')
    
    auth_status.short_description = "Authentication Status"
    
    def auth_actions(self, obj):
        """Display buttons for authentication actions."""
        actions = []
        
        # For objects that don't have an ID yet (new objects)
        if obj.pk is None:
            return format_html('<p>Save the configuration first to enable authentication actions.</p>')
        
        # Authentication button
        if not obj.authorized or not obj.refresh_token:
            url = reverse_lazy('external_integrations:auth_gmail_with_id', args=[obj.pk])
            actions.append(f'<a class="button" href="{url}">Authenticate with Google</a>')
        
        # Revoke button
        if obj.authorized and obj.refresh_token:
            url = reverse_lazy('external_integrations:revoke_auth', args=[obj.pk])
            actions.append(f'<a class="button" style="background: #d9534f; color: white;" href="{url}">Revoke Access</a>')
        
        # Test connection button
        if obj.authorized and obj.refresh_token:
            url = reverse_lazy('external_integrations:test_connection', args=[obj.pk])
            actions.append(f'<a class="button" style="background: #5bc0de; color: white;" href="{url}">Test Connection</a>')
        
        return format_html('<div style="display: flex; gap: 10px;">{}</div>'.format(''.join(actions)))
    
    auth_actions.short_description = "Authentication Actions"
    
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        # Limit to one authentication entry for simplicity
        return not GoogleAPIAuth.objects.exists()


admin.site.register(Integration, IntegrationAdmin)
admin.site.register(GoogleAPIAuth, GoogleAPIAuthAdmin)
