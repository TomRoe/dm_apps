# Generated by Django 2.1.4 on 2019-04-23 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0004_auto_20190326_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_code', models.IntegerField(choices=[(1, 'Nova Scotia'), (2, 'New Brunswick'), (3, 'Prince Edward Island'), (4, 'Quebec'), (5, 'Newfoundland')])),
                ('district_code', models.IntegerField()),
                ('port_code', models.IntegerField()),
                ('port_name', models.CharField(max_length=100)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('herring_fishing_area_code', models.CharField(max_length=100)),
                ('nafo_unit_area_code', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['province_code', 'district_code', 'port_code'],
            },
        ),
    ]