# Generated by Django 3.2.5 on 2021-12-09 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0003_csasrequest_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='csasrequestreview',
            name='email_notification_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='email notification date'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Ready for review'), (4, 'Under review'), (5, 'Fulfilled'), (6, 'Withdrawn'), (11, 'Reviewed'), (12, 'Flagged')], default=1, editable=False, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='csasrequestreview',
            name='decision',
            field=models.IntegerField(blank=True, choices=[(1, 'Screen in'), (2, 'Return to client'), (3, 'Re-scope')], null=True, verbose_name='recommendation'),
        ),
    ]