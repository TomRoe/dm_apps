# Generated by Django 2.2.2 on 2020-02-11 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0005_auto_20200211_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observationplatform',
            name='authority',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Authority'),
        ),
        migrations.AlterField(
            model_name='observationplatform',
            name='longname',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Long name'),
        ),
        migrations.AlterField(
            model_name='observationplatform',
            name='make_model',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Make and model'),
        ),
        migrations.AlterField(
            model_name='observationplatform',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Call name'),
        ),
        migrations.AlterField(
            model_name='observationplatform',
            name='observation_platform_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='platforms', to='vault.ObservationPlatformType', verbose_name='Type of observation platform'),
        ),
        migrations.AlterField(
            model_name='observationplatform',
            name='owner',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Owner'),
        ),
    ]