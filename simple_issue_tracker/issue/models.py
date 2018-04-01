from threading import Timer
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    access_token = models.TextField(null=True, blank=True)


class Issue(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='assigned_to', null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    status = models.CharField(max_length=100)


@receiver(post_save, sender=Issue)
def issue_created(sender, instance, created, **kwargs):
    email = instance.created_by.email
    print email
    if created:
        subject = 'Issue Created by ' + instance.created_by.first_name
        message = 'An Issue has been successfully created'
    else:
        subject = 'Issue Assigned to ' + instance.assigned_to.first_name
        message = 'An Issue created by ' + instance.created_by.first_name + ', has been assigned to ' + \
                  instance.assigned_to.first_name
    send = Timer(720, send_email, [subject, message, email])
    send.start()


def send_email(subject, message, email):
    print email
    print type(email)
    send_mail(
        subject,
        message,
        'surendrak@gowdanar.com',
        [email],
        fail_silently=False
    )