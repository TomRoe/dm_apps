# Generated by Django 2.2.2 on 2019-11-08 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0025_region_head'),
        ('travel', '0035_auto_20191108_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='event_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trip_events', to='shared_models.Region', verbose_name='Event / Meeting Lead'),
        ),
        migrations.AddField(
            model_name='trip',
            name='has_event_template',
            field=models.NullBooleanField(verbose_name='Is there an event template being completed for this conference or meeting?'),
        ),
    ]
