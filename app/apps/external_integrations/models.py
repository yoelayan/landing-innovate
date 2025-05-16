from django.db import models
from django.utils import timezone


class Integration(models.Model):
    # Head, footer
    UBICATIONS = [
        ("head", "Head"),
        ("footer", "Footer"),
    ]
    name = models.CharField(max_length=255)
    code = models.TextField()
    ubication = models.CharField(max_length=255, choices=UBICATIONS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Integracion"
        verbose_name_plural = "Integraciones"


class GoogleAPIAuth(models.Model):
    name = models.CharField(max_length=255, default="Gmail API")
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    refresh_token = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    authorized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(blank=True, null=True)
    
    def is_active(self):
        return self.authorized and self.refresh_token is not None
    
    def token_expired(self):
        if not self.token_expiry:
            return True
        return self.token_expiry < timezone.now()
    
    def use_token(self):
        self.last_used = timezone.now()
        self.save(update_fields=['last_used'])
    
    def __str__(self):
        return f"{self.name} ({self.id})"
    
    class Meta:
        verbose_name = "Google API Auth"
        verbose_name_plural = "Google API Authentications"
