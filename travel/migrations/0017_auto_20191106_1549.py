# Generated by Django 2.2.2 on 2019-11-06 19:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0025_region_head'),
        ('travel', '0016_auto_20191106_1548'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event',
            new_name='Trip',
        ),
    ]