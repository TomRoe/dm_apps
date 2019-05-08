# Generated by Django 2.1.4 on 2019-05-03 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shared_models', '0013_language'),
        ('masterlist', '0009_auto_20190503_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name (English)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (French)')),
                ('abbrev_eng', models.CharField(blank=True, max_length=255, null=True, verbose_name='abbreviation (French)')),
                ('abbrev_fre', models.CharField(blank=True, max_length=255, null=True, verbose_name='abbreviation (French)')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finance_id', models.CharField(blank=True, max_length=50, null=True)),
                ('tracking_system_id', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.TextField()),
                ('title_abbrev', models.CharField(blank=True, max_length=150, null=True)),
                ('project_length', models.IntegerField(blank=True, null=True)),
                ('risk_assessment_score', models.IntegerField(blank=True, choices=[(1, 'low'), (2, 'medium'), (3, 'high')], null=True)),
                ('date_completed', models.DateTimeField(blank=True, null=True)),
                ('requested_funding_y1', models.FloatField(blank=True, null=True, verbose_name='requested funding (year 1)')),
                ('requested_funding_y2', models.FloatField(blank=True, null=True, verbose_name='requested funding (year 2)')),
                ('requested_funding_y3', models.FloatField(blank=True, null=True, verbose_name='requested funding (year 3)')),
                ('regional_score', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('application_submission_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='project notes')),
                ('recommended_funding_y1', models.FloatField(blank=True, null=True, verbose_name='recommended funding (year 1)')),
                ('recommended_funding_y2', models.FloatField(blank=True, null=True, verbose_name='recommended funding (year 2)')),
                ('recommended_funding_y3', models.FloatField(blank=True, null=True, verbose_name='recommended funding (year 3)')),
                ('recommended_overprogramming', models.FloatField(blank=True, null=True)),
                ('negotiations_workplan_completion_date', models.DateTimeField(blank=True, null=True)),
                ('negotiations_financials_completion_date', models.DateTimeField(blank=True, null=True)),
                ('regrets_or_op_letter_sent_date', models.DateTimeField(blank=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='shared_models.Language', verbose_name='project language')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='masterlist.Organization')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='spot.Program')),
                ('regions', models.ManyToManyField(to='shared_models.Region')),
                ('start_year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gc_projects', to='shared_models.FiscalYear')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name (English)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (French)')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='spot.Status'),
        ),
    ]
