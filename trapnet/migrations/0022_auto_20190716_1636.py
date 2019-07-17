# Generated by Django 2.2.2 on 2019-07-16 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trapnet', '0021_auto_20190716_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='life_stage_eng',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='life stage name (English)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='life_stage_fre',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='life stage name (French)'),
        ),
    ]
