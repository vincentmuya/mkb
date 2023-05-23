# Generated by Django 4.1.3 on 2023-05-23 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_property_propertytype_type_delete_landlord_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='property',
            name='property_type',
        ),
        migrations.RemoveField(
            model_name='property',
            name='type',
        ),
        migrations.AlterUniqueTogether(
            name='propertytype',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='propertytype',
            name='parent',
        ),
        migrations.AlterUniqueTogether(
            name='type',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='type',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Property',
        ),
        migrations.DeleteModel(
            name='PropertyType',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
