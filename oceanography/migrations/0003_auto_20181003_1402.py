# Generated by Django 2.0.4 on 2018-10-03 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oceanography', '0002_auto_20181003_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='area_of_operation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]