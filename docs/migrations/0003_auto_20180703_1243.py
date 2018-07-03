# Generated by Django 2.0.4 on 2018-07-03 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0002_auto_20180703_1239'),
    ]

    operations = [
        migrations.CreateModel(
            name='section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='doc',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='docs.section'),
            preserve_default=False,
        ),
    ]
