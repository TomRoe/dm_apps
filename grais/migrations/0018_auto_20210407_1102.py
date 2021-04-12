# Generated by Django 3.1.6 on 2021-04-07 14:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grais', '0017_auto_20210401_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplespecies',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='samplespecies',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='samplespecies_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='samplespecies',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='samplespecies',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='samplespecies_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='probemeasurement',
            name='cloud_cover',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='cloud cover (%)'),
        ),
        migrations.AlterField(
            model_name='probemeasurement',
            name='ph',
            field=models.FloatField(blank=True, null=True, verbose_name=' pH'),
        ),
        migrations.AlterField(
            model_name='probemeasurement',
            name='sample',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='probe_data', to='grais.sample'),
        ),
        migrations.AlterField(
            model_name='probemeasurement',
            name='timezone',
            field=models.CharField(blank=True, choices=[('AST', 'AST'), ('ADT', 'ADT'), ('UTC', 'UTC')], default='ADT', max_length=5, null=True),
        ),
    ]
