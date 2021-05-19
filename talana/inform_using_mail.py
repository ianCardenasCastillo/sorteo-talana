from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from talana.settings import EMAIL_HOST_USER

def send_mail_to(subject, message, receiver):
    msg = EmailMultiAlternatives(subject=subject, from_email=EMAIL_HOST_USER,to=[receiver])
    msg.attach_alternative(message, "text/html")
    msg.send()