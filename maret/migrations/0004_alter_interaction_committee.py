# Generated by Django 3.2.4 on 2021-10-12 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maret', '0003_auto_20211006_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='committee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='committee_interactions', to='maret.committee', verbose_name='Committee / Working Group'),
        ),
    ]
