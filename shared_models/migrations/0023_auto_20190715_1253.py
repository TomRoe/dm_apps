# Generated by Django 2.2.2 on 2019-07-15 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0022_river_parent_river'),
    ]

    operations = [
        migrations.AlterField(
            model_name='river',
            name='cgndb',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]