# Generated by Django 2.1.4 on 2019-03-20 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dm_tickets', '0010_auto_20190320_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='fiscal_year',
        ),
    ]