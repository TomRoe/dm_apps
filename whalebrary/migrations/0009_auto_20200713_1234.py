# Generated by Django 2.2.2 on 2020-07-13 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whalebrary', '0008_auto_20200713_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='whalebrary.Transaction', verbose_name='transaction'),
        ),
    ]
