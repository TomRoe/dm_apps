# Generated by Django 3.2 on 2021-05-10 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whalebrary', '0005_add_resight_model'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlanningLinks',
            new_name='PlanningLink',
        ),
    ]