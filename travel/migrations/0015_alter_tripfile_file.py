# Generated by Django 3.2.5 on 2021-11-05 13:25

from django.db import migrations, models
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0014_tripfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripfile',
            name='file',
            field=models.FileField(null=True, upload_to=travel.models.trip_file_directory_path, verbose_name='attachment'),
        ),
    ]
