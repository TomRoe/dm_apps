# Generated by Django 3.2 on 2021-05-11 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0024_auto_20210507_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['process', 'title_en']},
        ),
    ]