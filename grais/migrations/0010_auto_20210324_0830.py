# Generated by Django 3.1.6 on 2021-03-24 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0009_auto_20210324_0830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incidentalreport',
            old_name='longitude_w',
            new_name='longitude',
        ),
    ]
