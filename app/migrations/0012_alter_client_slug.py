# Generated by Django 4.1.3 on 2023-07-24 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_loanhistory_id_number_loanhistory_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]