# Generated by Django 2.1.4 on 2019-05-10 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0026_auto_20190509_0936'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sample',
            options={'ordering': ['-season', 'date_deployed', 'station']},
        ),
        migrations.AddField(
            model_name='line',
            name='is_lost',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Was the line lost?'),
        ),
    ]