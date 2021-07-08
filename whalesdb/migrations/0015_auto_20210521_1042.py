# Generated by Django 3.2 on 2021-05-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whalesdb', '0014_alter_rcichannelinfo_rci_volts'),
    ]

    operations = [
        migrations.AddField(
            model_name='prjproject',
            name='lead',
            field=models.CharField(default='None', max_length=255, verbose_name='Project Lead/PI'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stestationevent',
            name='ste_depth_mcal',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True, verbose_name='MCAL Depth (m)'),
        ),
    ]