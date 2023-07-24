# Generated by Django 4.1.3 on 2023-07-23 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_loanhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanhistory',
            name='loan_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loanhistory',
            name='loan_collection_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]