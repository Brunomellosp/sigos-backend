from django.core.mail import send_mail
from django.conf import settings


def send_reset_password_email(email: str, reset_link: str):
    subject = "Recuperação de senha - SIGOS"
    message = f"Clique no link para redefinir sua senha: {reset_link}"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email], fail_silently=False)
