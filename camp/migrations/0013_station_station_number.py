# Generated by Django 2.0.4 on 2018-11-14 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0012_auto_20181113_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='station_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
