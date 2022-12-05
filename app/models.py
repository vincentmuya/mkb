from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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
