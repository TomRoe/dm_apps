# Generated by Django 2.1.4 on 2019-06-04 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='expected_purchase_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]