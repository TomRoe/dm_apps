# Generated by Django 3.1.2 on 2021-02-16 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0006_fix_blank_verbose_names'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outing',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='outing',
            name='start_time',
        ),
        migrations.AddField(
            model_name='outing',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End date and time (YYYY-MM-DD)'),
        ),
        migrations.AlterField(
            model_name='outing',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start date and time (YYYY-MM-DD)'),
        ),
    ]
