# Generated by Django 3.2.4 on 2021-09-29 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0024_person_expertise'),
        ('csas2', '0039_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='advice_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Target date for to provide Science advice'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Ready for review'), (4, 'Under review'), (5, 'Complete'), (11, 'Approved'), (12, 'Withdrawn')], default=1, editable=False, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='csasrequestreview',
            name='decision',
            field=models.IntegerField(blank=True, choices=[(1, 'Approved'), (2, 'Withdrawn')], null=True, verbose_name='decision'),
        ),
        migrations.AlterField(
            model_name='process',
            name='fiscal_year',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='processes', to='shared_models.fiscalyear', verbose_name='fiscal year'),
        ),
        migrations.AlterField(
            model_name='process',
            name='status',
            field=models.IntegerField(choices=[(1, 'Initiated'), (20, 'On'), (22, 'ToR Complete'), (25, 'Meeting Complete'), (30, 'Deferred'), (100, 'Complete'), (90, 'Withdrawn'), (2, 'temp-complete'), (3, 'temp-deferred'), (4, 'temp-delayed'), (5, 'temp-tentative')], default=1, verbose_name='status'),
        ),
    ]
