# Generated by Django 3.2.4 on 2021-10-01 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0041_termsofreference_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csasrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Ready for review'), (4, 'Under review'), (5, 'Complete'), (11, 'Accepted'), (12, 'Withdrawn')], default=1, editable=False, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='csasrequestreview',
            name='decision',
            field=models.IntegerField(blank=True, choices=[(1, 'Accepted'), (2, 'Withdrawn')], null=True, verbose_name='decision'),
        ),
        migrations.AlterField(
            model_name='process',
            name='status',
            field=models.IntegerField(choices=[(1, 'Initiated'), (20, 'On'), (22, 'ToR Complete'), (25, 'Meeting Complete'), (30, 'Deferred'), (100, 'Complete'), (90, 'Withdrawn')], default=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='termsofreference',
            name='is_complete',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Selecting yes will update the process status', verbose_name='Are the ToRs complete?'),
        ),
    ]