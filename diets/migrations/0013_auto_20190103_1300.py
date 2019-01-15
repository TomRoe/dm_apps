# Generated by Django 2.1.4 on 2019-01-03 17:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0012_auto_20190103_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predator',
            name='processing_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='processing date (dd-mm-yyyy)'),
        ),
    ]