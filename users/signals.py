from django.db.models.signals import post_save
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from django.dispatch import receiver
from .models import Profile

#signal to create a profile for all new users
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        #ensure a profile is created for each new user
        #profile, _ = Profile.objects.get_or_create(user=instance)
        profile = Profile.objects.create(user=instance)

        #assign object-level permissions
        assign_perm('view_profile', instance, profile)
        assign_perm('change_profile', instance, profile)