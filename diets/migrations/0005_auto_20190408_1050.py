# Generated by Django 2.1.4 on 2019-04-08 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0004_auto_20190401_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prey',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='prey_items', to='diets.Species'),
        ),
    ]
