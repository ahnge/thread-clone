from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MyUser


@receiver(post_save, sender=User)
def create_myuser(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_myuser(sender, instance, **kwargs):
    instance.myuser.save()
