# Generated by Django 3.1.2 on 2021-03-15 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fisheriescape', '0013_mm_risk_choices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fishery',
            old_name='fishery_area',
            new_name='fishery_areas',
        ),
    ]