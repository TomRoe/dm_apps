# Generated by Django 2.1.4 on 2019-02-28 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0017_auto_20190228_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consultationinstructionemailmembers',
            old_name='instructions',
            new_name='consultation_instruction',
        ),
        migrations.AlterUniqueTogether(
            name='consultationinstructionemailmembers',
            unique_together={('consultation_instruction', 'member')},
        ),
    ]
