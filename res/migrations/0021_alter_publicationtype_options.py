# Generated by Django 3.2.4 on 2021-10-20 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0020_auto_20211020_1245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicationtype',
            options={'ordering': ['code']},
        ),
    ]