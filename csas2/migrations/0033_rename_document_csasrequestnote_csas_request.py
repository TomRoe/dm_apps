# Generated by Django 3.2 on 2021-05-21 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0032_remove_csasrequest_remarks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csasrequestnote',
            old_name='document',
            new_name='csas_request',
        ),
    ]
