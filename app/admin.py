from django.contrib import admin
from .models import Client, Profile, LoanHistory

# Register your models here.
admin.site.register(Client)
admin.site.register(Profile)
admin.site.register(LoanHistory)
