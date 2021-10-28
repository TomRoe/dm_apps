# Generated by Django 3.2.4 on 2021-09-21 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0008_auto_20210817_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animaldetcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='containerdetcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='countcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='envcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='envsubjcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='envtreatcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='eventfilecode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='facilitycode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='feedcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='feedmethod',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='imagecode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='indtreatcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='instdetcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='instrumentcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='locationdetcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='loccode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='prioritycode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='protocode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='qualcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='rivercode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='rolecode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='samplecode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='spawndetcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='spawndetsubjcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='stockcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='unitcode',
            options={'ordering': ['name']},
        ),
    ]