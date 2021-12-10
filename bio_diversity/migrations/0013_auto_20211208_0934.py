# Generated by Django 3.2.5 on 2021-12-08 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0012_alter_sample_samp_num'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='pairing',
            name='Pairing_Uniqueness',
        ),
        migrations.RemoveConstraint(
            model_name='sample',
            name='Sample_Uniqueness',
        ),
        migrations.RemoveConstraint(
            model_name='sire',
            name='Sire_Uniqueness',
        ),
    ]