# Generated by Django 2.2.2 on 2020-02-21 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0007_sample_surface_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='surface_type',
            new_name='sample_type',
        ),
    ]
