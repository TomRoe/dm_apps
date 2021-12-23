# Generated by Django 3.1.2 on 2021-02-09 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20210209_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='email',
        ),
        migrations.AddField(
            model_name='event',
            name='from_email',
            field=models.EmailField(default='DoNotReply.DMApps@Azure.Cloud.dfo-mpo.gc.ca', max_length=254, verbose_name='FROM email address (on invitation)'),
        ),
        migrations.AddField(
            model_name='event',
            name='rsvp_email',
            field=models.EmailField(default=1, max_length=254, verbose_name='RSVP email address (on invitation)'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='invitee',
            unique_together={('event', 'email')},
        ),
    ]