# Generated by Django 2.2.2 on 2019-06-07 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0005_auto_20190606_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', to=settings.AUTH_USER_MODEL),
        ),
    ]