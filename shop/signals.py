from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer, Cart
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )


@receiver(post_save, sender=Customer)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)


@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        username = instance.username
        ac_link = "127.0.0.1:8000/activate"
        subject = "Activate Your Account"
        html_message = render_to_string(
            "registration_email.html",
            {"username": username, "activation_link": ac_link},
        )
        plain_message = strip_tags(html_message)
        from_email = "djtest1210@gmail.com"
        to_email = [instance.email]
        send_mail(
            subject, plain_message, from_email, to_email, html_message=html_message
        )
