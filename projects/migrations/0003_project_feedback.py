# Generated by Django 2.1.4 on 2019-01-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_fiscal_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='feedback',
            field=models.TextField(blank=True, null=True, verbose_name='Do you have any feedback you would like to submit about this process?'),
        ),
    ]