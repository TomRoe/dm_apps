# Generated by Django 3.1.2 on 2020-10-28 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0012_auto_20201028_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cruise',
            old_name='funding_project_ID',
            new_name='funding_project_id',
        ),
    ]