from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    if created:
        Profile.objects.create(user=instance)
