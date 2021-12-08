# Generated by Django 3.2.5 on 2021-12-02 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0030_remove_river_fishing_area_code'),
        ('maret', '0007_alter_interaction_interaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='dfo_role',
            field=models.IntegerField(choices=[(None, '---------'), (1, 'Programs'), (2, 'Manager'), (3, 'Director'), (4, 'Regional Director'), (5, 'Associate Regional Director General'), (6, 'Regional Director General'), (7, 'Director General'), (8, 'Assistant Deputy Minister'), (9, 'Senior Assistant Deputy Minister'), (10, 'Deputy Minister'), (11, 'Minister'), (12, 'Unknown')], default=12, verbose_name='Role of highest level DFO participant'),
        ),
        migrations.AddField(
            model_name='committee',
            name='main_topic',
            field=models.ManyToManyField(blank=True, related_name='committee_main_topics', to='maret.DiscussionTopic', verbose_name='Main Topic(s) of discussion'),
        ),
        migrations.AddField(
            model_name='committee',
            name='species',
            field=models.ManyToManyField(blank=True, related_name='committee_species', to='maret.Species', verbose_name='Main species of discussion'),
        ),
        migrations.AlterField(
            model_name='committee',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='committee_branch', to='shared_models.branch', verbose_name='Lead DFO branch / area office'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='dfo_role',
            field=models.IntegerField(choices=[(None, '---------'), (1, 'Programs'), (2, 'Manager'), (3, 'Director'), (4, 'Regional Director'), (5, 'Associate Regional Director General'), (6, 'Regional Director General'), (7, 'Director General'), (8, 'Assistant Deputy Minister'), (9, 'Senior Assistant Deputy Minister'), (10, 'Deputy Minister'), (11, 'Minister'), (12, 'Unknown')], default=None, verbose_name='Role of highest level DFO participant'),
        ),
    ]
