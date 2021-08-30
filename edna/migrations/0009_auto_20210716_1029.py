# Generated by Django 3.2.4 on 2021-07-16 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0008_alter_sample_bottle_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='collection date/time'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='edna.sampletype', verbose_name='sample type'),
            preserve_default=False,
        ),
    ]