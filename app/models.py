from django.db import models
from django.urls import reverse
from slugify import slugify


# Create your models here.
class Client(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True)
    id_number = models.IntegerField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    Residence = models.CharField(max_length=50)
    loan_collection_date = models.DateField(null=True, blank=True)
    loan_amount = models.IntegerField(null=True, blank=True)
    loan_interest = models.IntegerField(null=True, blank=True)
    loan_penalty = models.IntegerField(null=True, blank=True)
    loan_balance = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client_detail', args=[self.id, self.slug])
