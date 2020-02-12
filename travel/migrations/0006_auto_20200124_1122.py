# Generated by Django 2.2.2 on 2020-01-24 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_auto_20200124_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='conference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trip_requests', to='travel.Conference', verbose_name='conference / meeting'),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='fiscal_year',
            field=models.ForeignKey(blank=True, default=2020, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trip_requests', to='shared_models.FiscalYear', verbose_name='fiscal year'),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trip_requests', to='shared_models.Region', verbose_name='DFO region'),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='status',
            field=models.ForeignKey(default=8, limit_choices_to={'used_for': 2}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trip_requests', to='travel.Status', verbose_name='trip status'),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_trip_requests', to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user'),
        ),
    ]