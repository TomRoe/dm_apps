# Generated by Django 3.2.5 on 2021-11-30 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0010_auto_20211130_1004'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pairing',
            unique_together={('indv_id', 'samp_id', 'start_date')},
        ),
        migrations.AlterUniqueTogether(
            name='sire',
            unique_together={('indv_id', 'samp_id', 'pair_id')},
        ),
    ]
