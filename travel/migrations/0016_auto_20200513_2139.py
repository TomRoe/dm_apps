# Generated by Django 2.2.2 on 2020-05-14 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0015_auto_20200513_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reason',
            name='name',
            field=models.CharField(default='temp', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reason',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(default='temp', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='role',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]