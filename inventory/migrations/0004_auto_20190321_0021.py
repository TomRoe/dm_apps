# Generated by Django 2.1.4 on 2019-03-21 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_remove_resource_section'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='section1',
            new_name='section',
        ),
    ]