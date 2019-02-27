# Generated by Django 2.1.4 on 2019-02-26 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0042_auto_20190225_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deliverables_html',
            field=models.TextField(blank=True, null=True, verbose_name='Project deliverables'),
        ),
        migrations.AddField(
            model_name='project',
            name='description_html',
            field=models.TextField(blank=True, null=True, verbose_name='Project objective & description'),
        ),
        migrations.AddField(
            model_name='project',
            name='priorities_html',
            field=models.TextField(blank=True, null=True, verbose_name='Project-specific priorities'),
        ),
        migrations.AlterField(
            model_name='project',
            name='metadata_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='please provide link to metadata, if available'),
        ),
    ]