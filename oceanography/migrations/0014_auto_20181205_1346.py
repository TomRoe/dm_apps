# Generated by Django 2.0.4 on 2018-12-05 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oceanography', '0013_auto_20181205_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bottle',
            name='salinity',
        ),
        migrations.AddField(
            model_name='bottle',
            name='sal',
            field=models.FloatField(blank=True, null=True, verbose_name='Salinity'),
        ),
        migrations.AddField(
            model_name='institute',
            name='abbrev',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
