from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Landlord(models.Model):
    name = models.CharField(max_length=30)
    PROPERTY = (
        ('Flats/Apartments', 'Flats/Apartments'),
        ('Bungalow', 'Bungalow'),
    )
    property = models.CharField(max_length=30, choices=PROPERTY)
    tenant_unit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
