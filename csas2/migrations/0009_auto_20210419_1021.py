# Generated by Django 3.2 on 2021-04-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0008_auto_20210419_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='csasrequestreview',
            name='prioritization',
            field=models.IntegerField(blank=True, choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], null=True, verbose_name='prioritization'),
        ),
        migrations.AddField(
            model_name='csasrequestreview',
            name='prioritization_text',
            field=models.TextField(blank=True, null=True, verbose_name='prioritization notes'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Under review'), (11, 'On'), (12, 'Off'), (13, 'Withdrawn')], default=1, editable=False, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='csasrequestreview',
            name='decision',
            field=models.IntegerField(blank=True, choices=[(1, 'On'), (2, 'Off'), (3, 'Withdrawn')], null=True, verbose_name='decision'),
        ),
        migrations.AlterField(
            model_name='csasrequestreview',
            name='decision_text',
            field=models.TextField(blank=True, null=True, verbose_name='Decision explanation'),
        ),
    ]
