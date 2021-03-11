# Generated by Django 3.1.2 on 2021-03-10 19:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0007_remove_tray_facic_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tray',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
        migrations.AddField(
            model_name='tray',
            name='start_date',
            field=models.DateField(default=datetime.date(2021, 3, 10), verbose_name='Start Date'),
            preserve_default=False,
        ),
    ]
