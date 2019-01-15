# Generated by Django 2.1.4 on 2019-01-15 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20190114_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitalcost',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capital_costs', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='collaborativeagreement',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='gccost',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gc_costs', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='omcost',
            name='om_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='om_costs', to='projects.OMCategory', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='omcost',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='om_costs', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_members', to='projects.Project'),
        ),
    ]