# Generated by Django 3.2 on 2021-05-21 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0031_auto_20210521_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csasrequest',
            name='remarks',
        ),
    ]