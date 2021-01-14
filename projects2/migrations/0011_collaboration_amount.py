# Generated by Django 3.1.2 on 2021-01-12 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0010_collaboration'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaboration',
            name='amount',
            field=models.FloatField(default=0, verbose_name='G&C amount (CAD)'),
        ),
    ]
