from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse

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


class Type(MPTTModel):
    Type = (
        ('Sale', 'Sale'),
        ('Rental', 'Rental'),
    )
    type = models.CharField(max_length=30, choices=Type)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "types"

    def __str__(self):
        full_path = [self.type]
        k = self.parent
        while k is not None:
            full_path.append(k.type)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('property_by_type', args=[self.slug])


class PropertyType(MPTTModel):
    PROPERTY_Type = (
        ('Flats/Apartments', 'Flats/Apartments'),
        ('Bungalow', 'Bungalow'),
    )
    property_type = models.CharField(max_length=30, choices=PROPERTY_Type)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "property_types"

    def __str__(self):
        full_path = [self.property_type]
        k = self.parent
        while k is not None:
            full_path.append(k.property_type)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def __str__(self):
        return self.property_type

    def get_absolute_url(self):
        return reverse('property_by_property_type', args=[self.slug])


class Property(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING,)
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    type = models.ForeignKey('Type', related_name="properties", on_delete=models.CASCADE)
    property_type = models.ForeignKey('PropertyType', related_name="properties", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    tenant_unit = models.IntegerField(null=True, blank=True)
    available_units = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    images = models.FileField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Property, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('property_detail', args=[self.id, self.slug])

    @classmethod
    def search_by_title(cls, search_term):
        search_result = cls.objects.filter(title__icontains=search_term)
        return search_result

