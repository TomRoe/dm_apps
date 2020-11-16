# Generated by Django 3.1.2 on 2020-11-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0010_auto_20201029_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrynote',
            name='type',
            field=models.IntegerField(choices=[(1, 'Action'), (2, 'Next step'), (3, 'Comment'), (4, 'Follow-up (*)'), (5, 'Internal')]),
        ),
        migrations.AlterField(
            model_name='entryperson',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
    ]
