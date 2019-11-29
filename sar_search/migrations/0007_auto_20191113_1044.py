# Generated by Django 2.2.2 on 2019-11-13 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sar_search', '0006_auto_20191031_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='iucn_red_list_status',
            field=models.ForeignKey(blank=True, limit_choices_to={'used_for': 5}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='iucn_spp', to='sar_search.SpeciesStatus', verbose_name='IUCN Red Flag status 123'),
        ),
    ]