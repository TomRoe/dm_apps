# Generated by Django 2.2.2 on 2019-06-17 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0055_file_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['-date_uploaded']},
        ),
        migrations.RenameField(
            model_name='file',
            old_name='date_created',
            new_name='date_uploaded',
        ),
        migrations.AlterField(
            model_name='file',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by'),
        ),
    ]
