# Generated by Django 3.1.2 on 2020-11-24 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0023_auto_20201124_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='approver_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Approver comments'),
        ),
        migrations.AlterField(
            model_name='review',
            name='approval_status',
            field=models.IntegerField(blank=True, choices=[(1, 'approved'), (0, 'not approved'), (9, 'cancelled')], null=True, verbose_name='Approval status'),
        ),
    ]
