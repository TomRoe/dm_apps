# Generated by Django 2.2.2 on 2020-01-14 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0026_auto_20200107_1614'),
        ('projects', '0034_auto_20200114_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary of activity')),
                ('pressures', models.TextField(blank=True, null=True, verbose_name='pressures')),
            ],
        ),
        migrations.RemoveField(
            model_name='functionalgroup',
            name='program',
        ),
        migrations.DeleteModel(
            name='SectionNote',
        ),
        migrations.AddField(
            model_name='note',
            name='functional_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='projects.FunctionalGroup'),
        ),
        migrations.AddField(
            model_name='note',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='shared_models.Section'),
        ),
    ]