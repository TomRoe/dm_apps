# Generated by Django 3.1.2 on 2020-11-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cruises', '0009_helptext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
    ]
