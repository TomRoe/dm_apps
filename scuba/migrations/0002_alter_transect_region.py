# Generated by Django 3.2.5 on 2021-12-08 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transect',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transects', to='scuba.region', verbose_name='region'),
        ),
    ]