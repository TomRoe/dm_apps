# Generated by Django 2.2.2 on 2019-10-24 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_auto_20191018_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='approver_approval_status',
            new_name='rdg_approval_status',
        ),
        migrations.AlterField(
            model_name='event',
            name='fiscal_year',
            field=models.ForeignKey(blank=True, default=2020, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips', to='shared_models.FiscalYear', verbose_name='fiscal year'),
        ),
    ]