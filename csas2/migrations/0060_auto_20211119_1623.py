# Generated by Django 3.2.5 on 2021-11-19 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0028_alter_organization_uuid'),
        ('csas2', '0059_auto_20211119_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csasoffice',
            name='name',
        ),
        migrations.RemoveField(
            model_name='csasoffice',
            name='nom',
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='advice_fiscal_year',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_request_advice', to='shared_models.fiscalyear', verbose_name='advice FY'),
        ),
        migrations.AlterField(
            model_name='csasrequest',
            name='fiscal_year',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_requests', to='shared_models.fiscalyear', verbose_name='request FY'),
        ),
    ]
