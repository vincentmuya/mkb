# Generated by Django 4.1.3 on 2023-07-27 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_client_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanhistory',
            name='loan_balance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loanhistory',
            name='loan_interest',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
