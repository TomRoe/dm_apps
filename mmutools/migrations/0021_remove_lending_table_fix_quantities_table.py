# Generated by Django 2.2.2 on 2020-05-12 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmutools', '0020_fix_items_table_size_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantity',
            old_name='location',
            new_name='locations',
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='lent_id',
        ),
        migrations.AddField(
            model_name='quantity',
            name='lent_date',
            field=models.DateTimeField(blank=True, help_text='Format: YYYY-MM-DD HH:mm:ss', null=True, verbose_name='lent date'),
        ),
        migrations.AddField(
            model_name='quantity',
            name='lent_to',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='lent to'),
        ),
        migrations.AddField(
            model_name='quantity',
            name='return_date',
            field=models.DateTimeField(blank=True, help_text='Format: YYYY-MM-DD HH:mm:ss', null=True, verbose_name='expected return date'),
        ),
        migrations.DeleteModel(
            name='Lending',
        ),
    ]
