# Generated by Django 2.0.4 on 2018-11-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0026_auto_20181121_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='h2o_temperature_c',
            field=models.FloatField(blank=True, null=True, verbose_name='Water temperature (°C)'),
        ),
    ]