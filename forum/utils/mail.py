import email
import socket
import os
import logging

try:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.header import Header
except:
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEImage import MIMEImage
    from email.Header import Header

from django.core.mail import DNS_NAME
from smtplib import SMTP
from smtplib import SMTPRecipientsRefused
from forum import settings
from django.template import loader, Context, Template
from forum.utils.html import sanitize_html
from forum.context import application_settings
from forum.utils.html2text import HTML2Text
from threading import Thread
from lib.helpers import send_mail


def send_template_email(recipients, template, context, sender=None, reply_to=None):
    t = loader.get_template(template)
    context.update(dict(recipients=recipients, settings=settings, sender=sender, reply_to=reply_to))
    t.render(Context(context))


def create_connection():
    connection = SMTP(str(settings.EMAIL_HOST), str(settings.EMAIL_PORT),
                          local_hostname=DNS_NAME.get_fqdn())

    if bool(settings.EMAIL_USE_TLS):
        connection.ehlo()
        connection.starttls()
        connection.ehlo()

    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        connection.login(str(settings.EMAIL_HOST_USER), str(settings.EMAIL_HOST_PASSWORD))

    return connection


def create_and_send_mail_messages(messages, sender_data=None, reply_to=None):
    if not settings.EMAIL_HOST:
        return

    sender = Header(unicode("Google Portal"), 'utf-8')
    
    if sender_data == None:
        sender.append('<%s>' % unicode(settings.DEFAULT_FROM_EMAIL))
        sender = u'%s <%s>' % (unicode("Google Portal"), unicode(settings.DEFAULT_FROM_EMAIL))
    else:
        sender.append('<%s>' % unicode(sender_data['email']))
        sender = u'%s <%s>' % (unicode(sender_data['name']), unicode(sender_data['email']))
        
    
    if reply_to == None:
        reply_to = unicode(settings.DEFAULT_REPLY_TO_EMAIL)
    else:
        reply_to = unicode(reply_to)

    if sender is None:
        sender = str(settings.DEFAULT_FROM_EMAIL)


    for recipient, subject, html, text, media in messages:
        mail_subject = subject

        mail_body  = html

        mail_to = set([
            recipient.email,
        ])
   
        bcc = set()

        mail_from = sender

        attachments = list()

        send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

