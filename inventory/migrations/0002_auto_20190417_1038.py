# Generated by Django 2.1.4 on 2019-04-17 13:38

import dfo_sci_dm_site.custom_widgets
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='descr_eng',
            field=dfo_sci_dm_site.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Description (English)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='descr_fre',
            field=dfo_sci_dm_site.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Description (French)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='purpose_eng',
            field=dfo_sci_dm_site.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Purpose (English)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='purpose_fre',
            field=dfo_sci_dm_site.custom_widgets.OracleTextField(blank=True, null=True, verbose_name='Purpose (French)'),
        ),
    ]