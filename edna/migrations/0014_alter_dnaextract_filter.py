# Generated by Django 3.2.4 on 2021-07-16 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0013_auto_20210716_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dnaextract',
            name='filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='edna.filter'),
        ),
    ]
