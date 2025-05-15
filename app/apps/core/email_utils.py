"""
Email utilities for sending emails from the application.
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import logging

def send_templated_email(subject, template_name, context, recipient_list, from_email=None):
    """
    Send an email using a template.
    
    Args:
        subject (str): Email subject
        template_name (str): Path to the email template
        context (dict): Context data for the template
        recipient_list (list): List of recipients
        from_email (str, optional): Sender email. Defaults to settings.DEFAULT_FROM_EMAIL.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    # Use Django's send_mail function which works with any backend including Anymail
    try:
        # Create message
        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            recipient_list
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send with the configured backend (now Google OAuth)
        return email.send() > 0
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return False

def send_subscription_confirmation(email, request=None):
    """
    Send a confirmation email to a new subscriber.
    
    Args:
        email (str): Subscriber's email
        request (HttpRequest, optional): The current request for building URLs. Defaults to None.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    subject = "¡Gracias por suscribirte a Innova7e!"
    context = {
        'email': email,
    }
    return send_templated_email(
        subject,
        'emails/subscription_confirmation.html',
        context,
        [email]
    )

def send_contact_confirmation(message_obj, request=None):
    """
    Send a confirmation email to a contact form submitter.
    
    Args:
        message_obj (Messages): The message object
        request (HttpRequest, optional): The current request for building URLs. Defaults to None.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    subject = "¡Gracias por contactar con Innova7e!"
    
    # Get the display name of the service
    interest_service_display = dict(message_obj.SERVICES).get(message_obj.interest_service, message_obj.interest_service)
    
    context = {
        'name': message_obj.name,
        'email': message_obj.email,
        'message': message_obj.message,
        'interest_service': message_obj.interest_service,
        'interest_service_display': interest_service_display,
        'created_at': message_obj.created_at,
    }
    
    return send_templated_email(
        subject,
        'emails/contact_confirmation.html',
        context,
        [message_obj.email]
    )

def send_subscription_admin_notification(suscriptor_obj, request=None):
    """
    Send an admin notification about a new subscription.
    
    Args:
        suscriptor_obj (Suscriptor): The suscriptor object
        request (HttpRequest, optional): The current request for building URLs. Defaults to None.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    if not settings.ADMIN_EMAILS:
        return False
    
    subject = "Nueva suscripción en Innova7e"
    
    # Build admin URL
    admin_url = "https://innova7e.com/admin/"
    if request:
        current_site = get_current_site(request)
        admin_url = f"https://{current_site.domain}{reverse('admin:pages_suscriptor_changelist')}"
    
    context = {
        'email': suscriptor_obj.email,
        'created_at': suscriptor_obj.created_at,
        'admin_url': admin_url,
    }
    
    return send_templated_email(
        subject,
        'emails/new_subscription_admin.html',
        context,
        settings.ADMIN_EMAILS
    )

def send_message_admin_notification(message_obj, request=None):
    """
    Send an admin notification about a new contact message.
    
    Args:
        message_obj (Messages): The message object
        request (HttpRequest, optional): The current request for building URLs. Defaults to None.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    if not settings.ADMIN_EMAILS:
        return False
    
    subject = "Nuevo mensaje de contacto en Innova7e"
    
    # Get the display name of the service
    interest_service_display = dict(message_obj.SERVICES).get(message_obj.interest_service, message_obj.interest_service)
    
    # Build admin URL
    admin_url = "https://innova7e.com/admin/"
    if request:
        current_site = get_current_site(request)
        admin_url = f"https://{current_site.domain}{reverse('admin:pages_messages_changelist')}"
    
    context = {
        'name': message_obj.name,
        'email': message_obj.email,
        'message': message_obj.message,
        'interest_service': message_obj.interest_service,
        'interest_service_display': interest_service_display,
        'created_at': message_obj.created_at,
        'admin_url': admin_url,
    }
    
    return send_templated_email(
        subject,
        'emails/new_message_admin.html',
        context,
        settings.ADMIN_EMAILS
    )

def send_bulk_email_to_subscribers(subject, message, template_name='emails/newsletter.html', from_email=None):
    """
    Send bulk emails to subscribers.
    
    Args:
        subject (str): Email subject
        message (str): Email message body
        template_name (str, optional): Path to the email template. Defaults to 'emails/newsletter.html'.
        from_email (str, optional): Sender email. Defaults to settings.DEFAULT_FROM_EMAIL.
    
    Returns:
        tuple: (number of emails sent successfully, number of errors)
    """
    from apps.pages.models import Suscriptor
    
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    subscribers = Suscriptor.objects.all()
    success_count = 0
    error_count = 0
    
    for subscriber in subscribers:
        context = {
            'email': subscriber.email,
            'message': message,
            'unsubscribe_url': settings.SITE_URL + reverse('home'),  # You may want to create an unsubscribe view
        }
        logging.info(f"Sending email to {subscriber.email}")
        if send_templated_email(subject, template_name, context, [subscriber.email], from_email):
            success_count += 1
        else:
            error_count += 1
            logging.error(f"Error sending email to {subscriber.email}")
    
    return success_count, error_count 