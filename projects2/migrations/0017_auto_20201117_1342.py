# Generated by Django 3.1.2 on 2020-11-17 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0016_auto_20201116_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectyear',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Recommended'), (4, 'Approved'), (5, 'Denied'), (9, 'Cancelled')], default=1, editable=False),
        ),
    ]
