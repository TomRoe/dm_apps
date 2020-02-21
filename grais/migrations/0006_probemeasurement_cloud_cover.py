# Generated by Django 2.2.2 on 2020-02-21 19:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0005_remove_probemeasurement_tide_descriptor'),
    ]

    operations = [
        migrations.AddField(
            model_name='probemeasurement',
            name='cloud_cover',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='% cloud cover'),
        ),
    ]
