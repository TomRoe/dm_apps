# Generated by Django 2.2.2 on 2020-02-18 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0007_auto_20200213_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='English name')),
                ('abbrev_name', models.CharField(max_length=255, verbose_name='English abbreviated name')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='French name')),
                ('abbrev_nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='French abbreviated name')),
            ],
        ),
        migrations.RemoveField(
            model_name='observationplatform',
            name='authority',
        ),
        migrations.RemoveField(
            model_name='observationplatform',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='person',
            name='organisation',
        ),
    ]
