# Generated by Django 2.2.2 on 2019-11-21 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0038_auto_20191113_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='conference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips', to='travel.Conference', verbose_name='conference / meeting'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='departure_location',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='departure location (e.g., city, province, country)'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='destination',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='destination location (e.g., city, province, country)'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='event_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trip_events', to='shared_models.Region', verbose_name='Regional event lead'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='is_conference',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='is this a conference or meeting?'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='non_dfo_costs',
            field=models.FloatField(blank=True, null=True, verbose_name='Estimated non-DFO costs (CAD)'),
        ),
    ]