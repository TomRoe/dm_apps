# Generated by Django 3.2.4 on 2021-08-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0010_triprequest_needs_gov_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='benefit_to_dfo',
            field=models.TextField(blank=True, null=True, verbose_name='describe the benefits to DFO. (See help bubble for additional information.)'),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='objective_of_event',
            field=models.TextField(blank=True, null=True, verbose_name='describe the objective(s) related to this activity. (See help bubble for additional information.)'),
        ),
    ]
