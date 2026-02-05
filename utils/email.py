from django.core.mail import send_mail

from config import settings


def send_email(subject, message, to_email):
    to_email = to_email if isinstance(to_email, list) else [to_email, ]
    # 위에 1줄 if문이 이거임
    # if isinstance(to_email, list):
    #     to_email = to_email
    # else:
    #     to_email = [to_email, ]

    send_mail(subject, message, settings.EMAIL_HOST_USER, to_email)