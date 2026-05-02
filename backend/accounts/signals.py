from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models.profile import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile when a User is created.
    """
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Ensure a Profile exists for every User.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
