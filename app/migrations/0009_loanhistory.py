# Generated by Django 4.1.3 on 2023-07-23 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_client_is_loan_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_paid', models.DateField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
    ]