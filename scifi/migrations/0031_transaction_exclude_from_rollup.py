# Generated by Django 2.1.4 on 2019-02-22 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0030_auto_20190222_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='exclude_from_rollup',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Exclude from rollup'),
        ),
    ]
