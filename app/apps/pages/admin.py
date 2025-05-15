from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Brand, Suscriptor, SiteImages, Messages, Review, FAQ
from .forms import BulkEmailForm
from apps.core.email_utils import send_bulk_email_to_subscribers

class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "image_thumbnail")
    list_editable = ("order",)
    search_fields = ("name",)
    ordering = ("order",)

    def image_thumbnail(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.logo.url)
        return "No Image"

    image_thumbnail.short_description = "Thumbnail"

class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)
    actions = ['send_email_to_subscribers']

    def send_email_to_subscribers(self, request, queryset):
        """Admin action to send emails to selected subscribers"""
        if 'send' in request.POST:
            form = BulkEmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                
                # Get only the emails from the selected subscribers
                recipients = queryset.values_list('email', flat=True)
                
                # Send emails
                success_count = 0
                error_count = 0
                
                for email in recipients:
                    # We're using the bulk email function but sending only to selected subscribers
                    from apps.core.email_utils import send_templated_email
                    context = {
                        'email': email,
                        'message': message,
                        'unsubscribe_url': request.build_absolute_uri('/'),  # Placeholder
                    }
                    
                    if send_templated_email(subject, 'emails/newsletter.html', context, [email]):
                        success_count += 1
                    else:
                        error_count += 1
                
                self.message_user(
                    request, 
                    f"Correos enviados: {success_count}. Errores: {error_count}.",
                    messages.SUCCESS if error_count == 0 else messages.WARNING
                )
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = BulkEmailForm()
        
        # Return a confirmation page
        return render(
            request,
            'admin/send_email_form.html',
            {
                'form': form,
                'subscribers': queryset,
                'title': 'Enviar correo a suscriptores seleccionados',
            }
        )
    
    send_email_to_subscribers.short_description = "Enviar correo a los suscriptores seleccionados"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-newsletter/', self.admin_site.admin_view(self.send_newsletter_view), name='send-newsletter'),
        ]
        return custom_urls + urls
    
    def send_newsletter_view(self, request):
        """View to send newsletter to all subscribers"""
        if request.method == 'POST':
            form = BulkEmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                
                # Send email to all subscribers
                success_count, error_count = send_bulk_email_to_subscribers(subject, message)
                
                self.message_user(
                    request, 
                    f"Correos enviados: {success_count}. Errores: {error_count}.",
                    messages.SUCCESS if error_count == 0 else messages.WARNING
                )
                return redirect('admin:pages_suscriptor_changelist')
        else:
            form = BulkEmailForm()
        
        return render(
            request,
            'admin/send_email_form.html',
            {
                'form': form,
                'title': 'Enviar newsletter a todos los suscriptores',
                'is_newsletter': True,
            }
        )

class SiteImagesAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "image_thumbnail")
    search_fields = ("name", "code")
    list_filter = ("name",)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"

    image_thumbnail.short_description = "Thumbnail"

class MessagesAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "interest_service", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("interest_service", "created_at")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Contact Information", {"fields": ("name", "email")}),
        ("Message Details", {"fields": ("message", "interest_service", "created_at")}),
    )

# Configuración para administrar Reviews
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "created_at")
    search_fields = ("name", "comment")
    list_filter = ("rating", "created_at")
    readonly_fields = ("created_at",)
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"

    image_thumbnail.short_description = "Thumbnail"

# Configuración para administrar FAQ
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "created_at")
    search_fields = ("question", "answer")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

    

admin.site.register(Brand, BrandAdmin)
admin.site.register(Suscriptor, SuscriptorAdmin)
admin.site.register(SiteImages, SiteImagesAdmin)
admin.site.register(Messages, MessagesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FAQ, FAQAdmin)