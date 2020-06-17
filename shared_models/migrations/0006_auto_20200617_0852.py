# Generated by Django 2.2.2 on 2020-06-17 11:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0005_auto_20200526_2100'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='branch',
        #     name='uuid',
        #     field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        # ),
        # migrations.AddField(
        #     model_name='division',
        #     name='uuid',
        #     field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        # ),
        # migrations.AddField(
        #     model_name='province',
        #     name='uuid',
        #     field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        # ),
        # migrations.AddField(
        #     model_name='region',
        #     name='uuid',
        #     field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        # ),
        # migrations.AddField(
        #     model_name='section',
        #     name='uuid',
        #     field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        # ),
        # migrations.AlterField(
        #     model_name='branch',
        #     name='date_last_modified',
        #     field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='date last modified'),
        #     preserve_default=False,
        # ),
        # migrations.AlterField(
        #     model_name='branch',
        #     name='name',
        #     field=models.CharField(max_length=255, verbose_name='name (en)'),
        # ),
        # migrations.AlterField(
        #     model_name='branch',
        #     name='nom',
        #     field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)'),
        # ),
        migrations.AlterField(
            model_name='cruise',
            name='mission_number',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='division',
            name='date_last_modified',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='date last modified'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name (en)'),
        ),
        migrations.AlterField(
            model_name='division',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)'),
        ),
        migrations.AlterField(
            model_name='province',
            name='date_last_modified',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='date last modified'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(default='temp', max_length=255, unique=True, verbose_name='name (en)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='province',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)'),
        ),
        migrations.AlterField(
            model_name='region',
            name='date_last_modified',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='date last modified'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name (en)'),
        ),
        migrations.AlterField(
            model_name='region',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)'),
        ),
        migrations.AlterField(
            model_name='section',
            name='date_last_modified',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='date last modified'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name (en)'),
        ),
        migrations.AlterField(
            model_name='section',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)'),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='call_sign',
            field=models.CharField(blank=True, max_length=56, null=True, unique=True),
        ),
    ]
