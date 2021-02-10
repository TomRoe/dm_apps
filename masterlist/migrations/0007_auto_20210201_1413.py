# Generated by Django 3.1.2 on 2021-02-01 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0006_auto_20210201_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='locked_by_ihub',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='organizationmember',
            name='locked_by_ihub',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='locked_by_ihub',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
