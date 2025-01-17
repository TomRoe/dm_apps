# Generated by Django 3.1.2 on 2021-03-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20210303_1001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='defaultreviewer',
            options={'ordering': ['user__first_name']},
        ),
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='faq',
            name='order',
            field=models.IntegerField(blank=True, null=True, verbose_name='display order'),
        ),
        migrations.AlterField(
            model_name='reviewer',
            name='role',
            field=models.IntegerField(choices=[(1, 'Reviewer'), (2, 'Recommender'), (3, 'NCR Travel Coordinators'), (4, 'ADM Recommender'), (5, 'ADM'), (6, 'Expenditure Initiation'), (7, 'RDG (Expenditure Initiation)')], verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='reviewer',
            name='status',
            field=models.IntegerField(choices=[(4, 'Draft'), (20, 'Queued'), (1, 'Pending'), (2, 'Approved'), (3, 'Denied'), (5, 'Cancelled'), (21, 'Skipped')], default=4, verbose_name='review status'),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='status',
            field=models.IntegerField(choices=[(8, 'Draft'), (17, 'Pending Review'), (12, 'Pending Recommendation'), (14, 'Pending ADM Approval'), (15, 'Pending Expenditure Initiation'), (16, 'Changes Requested'), (10, 'Denied'), (11, 'Approved'), (22, 'Cancelled')], default=8, editable=False, verbose_name='trip request status'),
        ),
    ]
