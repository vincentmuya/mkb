from django.contrib import admin
from .models import Property, PropertyType, Type, Profile


# Register your models here.
admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(Type)
admin.site.register(Profile)
