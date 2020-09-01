# Generated by Django 2.2.2 on 2020-08-27 15:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engagements', '0007_auto_20200825_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteractionObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InteractionSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='engagementplan',
            name='staff_collaborators',
            field=models.ManyToManyField(blank=True, related_name='engagement_plan_collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='engagementplan',
            name='stakeholders',
            field=models.ManyToManyField(blank=True, to='engagements.Organization'),
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='objectives',
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='subjects',
        ),
        migrations.AddField(
            model_name='interaction',
            name='objectives',
            field=models.ManyToManyField(related_name='interaction_objectives', to='engagements.InteractionObjective'),
        ),
        migrations.AddField(
            model_name='interaction',
            name='subjects',
            field=models.ManyToManyField(related_name='interaction_subjects', to='engagements.InteractionSubject'),
        ),
    ]
