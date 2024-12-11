from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    rooms_uploaded = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"User {self.user.username}  ({self.user.pk}) "

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.profile:
        instance.profile.save()
        


class Room(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    price = models.IntegerField()
    thumbnail = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
