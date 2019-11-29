# Generated by Django 2.2.2 on 2019-11-07 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0027_auto_20191107_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewer',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewers', to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user'),
        ),
    ]