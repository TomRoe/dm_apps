# Generated by Django 2.1.4 on 2019-03-26 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oceanography', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='institute',
        ),
        migrations.RemoveField(
            model_name='mission',
            name='probe',
        ),
        migrations.RemoveField(
            model_name='mission',
            name='vessel',
        ),
        migrations.AlterField(
            model_name='bottle',
            name='mission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bottles', to='shared_models.Cruise'),
        ),
        migrations.AlterField(
            model_name='file',
            name='mission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='shared_models.Cruise'),
        ),
        migrations.DeleteModel(
            name='Institute',
        ),
        migrations.DeleteModel(
            name='Mission',
        ),
        migrations.DeleteModel(
            name='Probe',
        ),
        migrations.DeleteModel(
            name='Vessel',
        ),
    ]