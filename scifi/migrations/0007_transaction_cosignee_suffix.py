# Generated by Django 2.2.2 on 2019-06-26 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0006_auto_20190607_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='cosignee_suffix',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='cosignee suffix'),
        ),
    ]