# Generated by Django 3.1.2 on 2021-03-15 10:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0003_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extractionbatch',
            options={'verbose_name_plural': 'DNA Extraction Batches'},
        ),
        migrations.AlterModelOptions(
            name='filtrationbatch',
            options={'verbose_name_plural': 'Filtration Batches'},
        ),
        migrations.AlterModelOptions(
            name='pcrbatch',
            options={'verbose_name_plural': 'PCR Batches'},
        ),
        migrations.AlterModelOptions(
            name='sample',
            options={'ordering': ['collection', 'unique_sample_identifier']},
        ),
        migrations.AlterField(
            model_name='extractionbatch',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='extractionbatch',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date/time'),
        ),
        migrations.AlterField(
            model_name='filtrationbatch',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='filtrationbatch',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date/time'),
        ),
        migrations.AlterField(
            model_name='pcrbatch',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='pcrbatch',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date/time'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='longitude'),
        ),
    ]
