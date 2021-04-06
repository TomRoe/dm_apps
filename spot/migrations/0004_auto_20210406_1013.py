# Generated by Django 3.1.6 on 2021-04-06 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0006_auto_20210225_1538'),
        ('spot', '0003_auto_20210106_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_year',
            field=models.ForeignKey(default=2023, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gc_projects', to='shared_models.fiscalyear'),
        ),
    ]
