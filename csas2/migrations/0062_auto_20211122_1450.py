# Generated by Django 3.2.5 on 2021-11-22 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0061_auto_20211122_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csasadminuser',
            name='region',
        ),
        migrations.AddField(
            model_name='csasrequest',
            name='office',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_offices', to='csas2.csasoffice', verbose_name='CSAS office'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='process',
            name='lead_office',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_lead_offices', to='csas2.csasoffice', verbose_name='CSAS office'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='process',
            name='other_offices',
            field=models.ManyToManyField(blank=True, to='csas2.CSASOffice', verbose_name='other CSAS offices'),
        ),
        migrations.AlterField(
            model_name='csasoffice',
            name='disable_request_notifications',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='disable notifications (request only)?'),
        ),
    ]
