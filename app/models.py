from django.db import models
from django.urls import reverse
from slugify import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save



# Create your models here.
class Client(models.Model):
    lender = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
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

    @classmethod
    def search_by_id_number(cls, search_term):
        search_result = cls.objects.filter(id_number__icontains=search_term)
        return search_result

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def save_profile(self):
        self.save()

    def __str__(self):
        return self.user

    @classmethod
    def this_profile(cls):
        profile = cls.objects.all()
        return profile

def Create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(Create_profile, sender=User)