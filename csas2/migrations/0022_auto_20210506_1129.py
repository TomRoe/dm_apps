# Generated by Django 3.2 on 2021-05-06 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0021_auto_20210506_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='termsofreference',
            name='expected_publications_en',
        ),
        migrations.RemoveField(
            model_name='termsofreference',
            name='expected_publications_fr',
        ),
    ]
