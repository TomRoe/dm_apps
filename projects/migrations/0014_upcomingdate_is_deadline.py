# Generated by Django 2.2.2 on 2020-06-17 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_upcomingdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcomingdate',
            name='is_deadline',
            field=models.BooleanField(default=False),
        ),
    ]