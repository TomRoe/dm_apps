# Generated by Django 3.1.2 on 2021-03-17 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0017_auto_20210317_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(help_text='Each planet revolves round the Sun in an elliptical orbit with the Sun at one focus. The straight line joining the Sun and the planet sweeps out equal areas in equal intervals. The squares of the orbital periods of planets are proportional to the cubes of their mean distance from the Sun.', max_length=1000, verbose_name='name'),
        ),
    ]
