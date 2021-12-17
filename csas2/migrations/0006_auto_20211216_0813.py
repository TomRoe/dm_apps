# Generated by Django 3.2.10 on 2021-12-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0005_alter_csasrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='termsofreference',
            name='posting_notification_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Posting notification date'),
        ),
        migrations.AddField(
            model_name='termsofreference',
            name='posting_request_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date of posting request'),
        ),
        migrations.AddField(
            model_name='termsofreference',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Ready for review'), (4, 'Under review'), (5, 'Fulfilled'), (6, 'Withdrawn'), (11, 'Reviewed'), (12, 'Flagged'), (13, 'Re-scoping')], default=1, editable=False, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='termsofreference',
            name='submission_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='submission date'),
        ),
    ]