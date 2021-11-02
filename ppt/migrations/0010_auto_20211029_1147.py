# Generated by Django 3.2.4 on 2021-10-29 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0028_alter_organization_uuid'),
        ('ppt', '0009_auto_20211027_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pptadminuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ppt_admin_user', to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='allotment_code',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects_ppt', to='shared_models.allotmentcode', verbose_name='allotment code (if known)'),
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='responsibility_center',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects_ppt', to='shared_models.responsibilitycenter', verbose_name='responsibility center (if known)'),
        ),
        migrations.AlterField(
            model_name='statusreport',
            name='project_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='ppt.projectyear'),
        ),
    ]