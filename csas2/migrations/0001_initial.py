# Generated by Django 3.2 on 2021-04-30 13:21

import csas2.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0013_auto_20210430_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_lead', models.BooleanField(default=False, verbose_name='lead author?')),
            ],
            options={
                'ordering': ['person__first_name', 'person__last_name'],
            },
        ),
        migrations.CreateModel(
            name='CSASRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_carry_over', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Is this request a carry-over from a previous year?')),
                ('language', models.IntegerField(choices=[(1, 'English'), (2, 'French')], default=1, verbose_name='language of request')),
                ('title', models.CharField(max_length=1000, verbose_name='title')),
                ('translated_title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='translated title')),
                ('is_multiregional', models.BooleanField(default=False, verbose_name='Does this request involve more than one region (zonal) or more than one client sector?')),
                ('multiregional_text', models.TextField(blank=True, null=True, verbose_name='Please provide the contact name, sector, and region for all involved.')),
                ('issue', models.TextField(blank=True, help_text='Should be phrased as a question to be answered by Science', null=True, verbose_name='Issue requiring science information and/or advice')),
                ('had_assistance', models.BooleanField(default=False, help_text='E.g. with CSAS and/or DFO science staff.', verbose_name='Have you had assistance from Science in developing the question/request?')),
                ('assistance_text', models.TextField(blank=True, null=True, verbose_name=' Please provide details about the assistance received')),
                ('rationale', models.TextField(blank=True, help_text='What will the information/advice be used for? Who will be the end user(s)? Will it impact other DFO programs or regions?', null=True, verbose_name='Rationale or context for the request')),
                ('risk_text', models.TextField(blank=True, null=True, verbose_name='What is the expected consequence if science advice is not provided?')),
                ('advice_needed_by', models.DateTimeField(verbose_name='Latest possible date to receive Science advice')),
                ('rationale_for_timeline', models.TextField(blank=True, help_text='e.g., COSEWIC or consultation meetings, Environmental Assessments, legal or regulatory requirement, Treaty obligation, international commitments, etc).Please elaborate and provide anticipatory dates', null=True, verbose_name='Rationale for deadline?')),
                ('has_funding', models.BooleanField(default=False, help_text='i.e., special analysis, meeting costs, translation)?', verbose_name='Do you have funds to cover any extra costs associated with this request?')),
                ('funding_text', models.TextField(blank=True, null=True, verbose_name='Please describe')),
                ('prioritization', models.IntegerField(blank=True, choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], null=True, verbose_name='How would you classify the prioritization of this request?')),
                ('prioritization_text', models.TextField(blank=True, null=True, verbose_name='What is the rationale behind the prioritization?')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Under review'), (4, 'Complete'), (11, 'On'), (12, 'Off'), (13, 'Withdrawn'), (14, 'Deferred')], default=1, editable=False, verbose_name='status')),
                ('submission_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='submission date')),
                ('old_id', models.IntegerField(blank=True, editable=False, null=True)),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True, verbose_name='unique identifier')),
                ('ref_number', models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='reference number')),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_client_requests', to=settings.AUTH_USER_MODEL, verbose_name='DFO client')),
                ('coordinator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_coordinator_requests', to=settings.AUTH_USER_MODEL, verbose_name='Regional CSAS coordinator')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csasrequest_created_by', to=settings.AUTH_USER_MODEL)),
                ('fiscal_year', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_requests', to='shared_models.fiscalyear', verbose_name='fiscal year')),
                ('section', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_requests', to='shared_models.section', verbose_name='section')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csasrequest_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'CSAS Requests',
                'ordering': ('fiscal_year', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(1, 'Meeting Minutes'), (2, 'Science Advisory Report'), (3, 'Research Document'), (4, 'Proceedings'), (5, 'Science Response'), (6, 'Working Paper'), (7, 'Term of Reference')], verbose_name='type')),
                ('title_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='title (English)')),
                ('title_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name='title (French)')),
                ('title_in', models.CharField(blank=True, max_length=255, null=True, verbose_name='title (Inuktitut)')),
                ('year', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999)], verbose_name='Publication Year')),
                ('pub_number', models.CharField(blank=True, max_length=25, null=True, verbose_name='publication number')),
                ('pages', models.IntegerField(blank=True, null=True, verbose_name='pages')),
                ('hide_from_list', models.BooleanField(default=False, verbose_name='This record should be hidden from the main search page')),
                ('file_en', models.FileField(blank=True, null=True, upload_to=csas2.models.doc_directory_path, verbose_name='file attachment (en)')),
                ('file_fr', models.FileField(blank=True, null=True, upload_to=csas2.models.doc_directory_path, verbose_name='file attachment (fr)')),
                ('url_en', models.URLField(blank=True, max_length=2000, null=True, verbose_name='document url (en)')),
                ('url_fr', models.URLField(blank=True, max_length=2000, null=True, verbose_name='document url (fr)')),
                ('dev_link_en', models.URLField(blank=True, max_length=2000, null=True, verbose_name='dev link (en)')),
                ('dev_link_fr', models.URLField(blank=True, max_length=2000, null=True, verbose_name='dev link (fr)')),
                ('ekme_gcdocs_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='EKME# / GCDocs (en)')),
                ('ekme_gcdocs_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name='EKME# / GCDocs (fr)')),
                ('lib_cat_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='library catalogue # (en)')),
                ('lib_cat_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name='library catalogue # (fr)')),
                ('status', models.IntegerField(choices=[(1, 'OK'), (2, 'In preparation'), (3, 'Submitted'), (4, 'Under review'), (5, 'In translation'), (6, 'Translated'), (7, 'Posted')], default=1, editable=False, verbose_name='status')),
                ('old_id', models.IntegerField(blank=True, editable=False, null=True)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='document_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InviteeRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(1, 'Steering Committee Meeting'), (2, 'Science Management Meeting'), (3, 'Advisory Process Meeting (RAP)'), (4, 'Science Response Meeting')], verbose_name='type of meeting')),
                ('is_virtual', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Is this a virtual meeting?')),
                ('location', models.CharField(blank=True, help_text='City, State/Province, Country or Virtual', max_length=1000, null=True, verbose_name='location')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='initial activity date')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='anticipated end date')),
                ('hide_from_list', models.BooleanField(default=False, verbose_name='This record should be hidden from the main search page')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meeting_created_by', to=settings.AUTH_USER_MODEL)),
                ('fiscal_year', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meetings', to='shared_models.fiscalyear', verbose_name='fiscal year')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True, verbose_name='unique identifier')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='title (en)')),
                ('nom', models.CharField(blank=True, max_length=1000, null=True, verbose_name='title (fr)')),
                ('status', models.IntegerField(choices=[(1, 'In-progress'), (2, 'Complete'), (3, 'Deferred'), (4, 'Delayed'), (5, 'Tentative')], default=1, verbose_name='status')),
                ('scope', models.IntegerField(choices=[(1, 'Regional'), (2, 'Zonal'), (3, 'National')], verbose_name='scope')),
                ('type', models.IntegerField(choices=[(1, 'Advisory Meeting'), (2, 'Science Response Process'), (3, 'Peer Review')], verbose_name='type')),
                ('context', models.TextField(blank=True, null=True, verbose_name='context')),
                ('objectives', models.TextField(blank=True, null=True, verbose_name='objectives')),
                ('expected_publications', models.TextField(blank=True, null=True, verbose_name='expected publications')),
                ('advisors', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='DFO Science advisors')),
                ('coordinator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csas_coordinator_processes', to=settings.AUTH_USER_MODEL, verbose_name='Lead coordinator')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='process_created_by', to=settings.AUTH_USER_MODEL)),
                ('csas_requests', models.ManyToManyField(blank=True, related_name='processes', to='csas2.CSASRequest', verbose_name='Connected CSAS requests')),
                ('fiscal_year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='processes', to='shared_models.fiscalyear', verbose_name='fiscal year')),
                ('lead_region', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='process_lead_regions', to='shared_models.region', verbose_name='lead region')),
                ('other_regions', models.ManyToManyField(blank=True, to='shared_models.Region', verbose_name='other regions')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='process_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['fiscal_year', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TermsOfReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('context_en', models.TextField(blank=True, help_text='English', null=True, verbose_name='context (en)')),
                ('context_fr', models.TextField(blank=True, help_text='French', null=True, verbose_name='context (fr)')),
                ('objectives_en', models.TextField(blank=True, help_text='English', null=True, verbose_name='objectives (en)')),
                ('objectives_fr', models.TextField(blank=True, help_text='French', null=True, verbose_name='objectives (fr)')),
                ('expected_publications_en', models.TextField(blank=True, help_text='English', null=True, verbose_name='expected publications (en)')),
                ('expected_publications_fr', models.TextField(blank=True, help_text='French', null=True, verbose_name='expected publications (fr)')),
                ('participation_en', models.TextField(blank=True, help_text='English', null=True, verbose_name='participation (en)')),
                ('participation_fr', models.TextField(blank=True, help_text='French', null=True, verbose_name='participation (fr)')),
                ('references_en', models.TextField(blank=True, help_text='English', null=True, verbose_name='references (en)')),
                ('references_fr', models.TextField(blank=True, help_text='French', null=True, verbose_name='references (fr)')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='termsofreference_created_by', to=settings.AUTH_USER_MODEL)),
                ('meeting', models.OneToOneField(blank=True, help_text='The ToR will pull several fields from the linked meeting (e.g., dates, chair, location, ...)', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tor', to='csas2.meeting', verbose_name='Linked to which meeting?')),
                ('process', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='tor', to='csas2.process')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='termsofreference_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeetingResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name (en)')),
                ('url_en', models.URLField(blank=True, max_length=2000, null=True, verbose_name='url (English)')),
                ('url_fr', models.URLField(blank=True, max_length=2000, null=True, verbose_name='url (French)')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meetingresource_created_by', to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='csas2.meeting')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meetingresource_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MeetingNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(1, 'To Do'), (2, 'Next step'), (3, 'General comment')], verbose_name='type')),
                ('note', models.TextField(verbose_name='note')),
                ('is_complete', models.BooleanField(default=False, verbose_name='complete?')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meetingnote_created_by', to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='csas2.meeting')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meetingnote_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['is_complete', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeetingFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=csas2.models.meeting_directory_path)),
                ('meeting', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='csas2.meeting')),
            ],
            options={
                'ordering': ['-date_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeetingCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_category', models.IntegerField(choices=[(1, 'Translation'), (2, 'Travel'), (3, 'Hospitality'), (4, 'Space rental'), (9, 'Other')], verbose_name='cost category')),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('funding_source', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.FloatField(default=0, verbose_name='amount (CAD)')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='csas2.meeting')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='process',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='csas2.process', verbose_name='process'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meeting_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Invitee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Invited'), (1, 'Accepted'), (2, 'Declined'), (3, 'Tentative')], default=0, verbose_name='status')),
                ('invitation_sent_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='date invitation was sent')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitees', to='csas2.meeting')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_invites', to='shared_models.person')),
                ('resources_received', models.ManyToManyField(editable=False, to='csas2.MeetingResource')),
                ('roles', models.ManyToManyField(to='csas2.InviteeRole', verbose_name='Function(s)')),
            ],
            options={
                'ordering': ['person__first_name', 'person__last_name'],
                'unique_together': {('meeting', 'person')},
            },
        ),
        migrations.CreateModel(
            name='DocumentTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='product due date')),
                ('submission_date', models.DateTimeField(blank=True, null=True, verbose_name='date submitted to CSAS office by author')),
                ('date_chair_sent', models.DateTimeField(blank=True, null=True, verbose_name='date sent to chair')),
                ('date_chair_appr', models.DateTimeField(blank=True, null=True, verbose_name='date approved by chair')),
                ('date_coordinator_sent', models.DateTimeField(blank=True, null=True, verbose_name='date sent to CSAS coordinator')),
                ('date_coordinator_appr', models.DateTimeField(blank=True, null=True, verbose_name='date approved by CSAS coordinator')),
                ('date_director_sent', models.DateTimeField(blank=True, null=True, verbose_name='date sent to director')),
                ('date_director_appr', models.DateTimeField(blank=True, null=True, verbose_name='date approved by director')),
                ('date_number_requested', models.DateTimeField(blank=True, null=True, verbose_name='date number requested')),
                ('number_approved', models.DateTimeField(blank=True, null=True, verbose_name='date number approved')),
                ('date_doc_submitted', models.DateTimeField(blank=True, null=True, verbose_name='date document submitted to CSAS office')),
                ('date_proof_author_sent', models.DateTimeField(blank=True, null=True, verbose_name='date PDF proof sent to author')),
                ('date_proof_author_approved', models.DateTimeField(blank=True, null=True, verbose_name='date PDF proof approved by author')),
                ('anticipated_posting_date', models.DateTimeField(blank=True, null=True, verbose_name='anticipated posting date')),
                ('actual_posting_date', models.DateTimeField(blank=True, null=True, verbose_name='actual posting date')),
                ('updated_posting_date', models.DateTimeField(blank=True, null=True, verbose_name='updated posting date')),
                ('date_translation_sent', models.DateTimeField(blank=True, null=True, verbose_name='date sent to translation')),
                ('is_review_complete', models.BooleanField(default=True, verbose_name='has the CSA office completed a translation review?')),
                ('client_ref_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='client reference number')),
                ('translation_ref_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='translation reference number')),
                ('is_urgent', models.BooleanField(default=True, verbose_name='was submitted as an urgent request?')),
                ('date_returned', models.DateTimeField(blank=True, null=True, verbose_name='date back from translation')),
                ('invoice_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='invoice number')),
                ('translation_notes', models.TextField(blank=True, null=True, verbose_name='translation notes')),
                ('chair', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_chair_positions', to='shared_models.person', verbose_name='chairperson')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documenttracking_created_by', to=settings.AUTH_USER_MODEL)),
                ('director', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_directors', to='shared_models.person', verbose_name='director')),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tracking', to='csas2.document')),
                ('proof_sent_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_proof_sent', to='shared_models.person', verbose_name='proof will be sent to which author')),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_submissions', to='shared_models.person', verbose_name='submitted by')),
                ('target_lang', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.language', verbose_name='target language')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documenttracking_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(1, 'To Do'), (2, 'Next step'), (3, 'General comment')], verbose_name='type')),
                ('note', models.TextField(verbose_name='note')),
                ('is_complete', models.BooleanField(default=False, verbose_name='complete?')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documentnote_created_by', to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='csas2.document')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documentnote_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['is_complete', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_category', models.IntegerField(choices=[(1, 'Translation'), (2, 'Travel'), (3, 'Hospitality'), (4, 'Space rental'), (9, 'Other')], verbose_name='cost category')),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('funding_source', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.FloatField(default=0, verbose_name='amount (CAD)')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='csas2.document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='document',
            name='meetings',
            field=models.ManyToManyField(blank=True, editable=False, related_name='documents', to='csas2.Meeting', verbose_name='csas meeting linkages'),
        ),
        migrations.AddField(
            model_name='document',
            name='people',
            field=models.ManyToManyField(editable=False, through='csas2.Author', to='shared_models.Person', verbose_name='authors'),
        ),
        migrations.AddField(
            model_name='document',
            name='process',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='csas2.process'),
        ),
        migrations.AddField(
            model_name='document',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='csas2.series', verbose_name='series'),
        ),
        migrations.AddField(
            model_name='document',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='document_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CSASRequestReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ref_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='reference number (optional)')),
                ('prioritization', models.IntegerField(blank=True, choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], null=True, verbose_name='prioritization')),
                ('prioritization_text', models.TextField(blank=True, null=True, verbose_name='prioritization notes')),
                ('decision', models.IntegerField(blank=True, choices=[(1, 'On'), (2, 'Off'), (3, 'Withdrawn'), (4, 'Deferred')], null=True, verbose_name='decision')),
                ('decision_text', models.TextField(blank=True, null=True, verbose_name='Decision explanation')),
                ('decision_date', models.DateTimeField(blank=True, null=True, verbose_name='decision date')),
                ('advice_date', models.DateTimeField(blank=True, null=True, verbose_name='date to provide Science advice')),
                ('is_deferred', models.BooleanField(default=False, verbose_name='was the original request date deferred?')),
                ('deferred_text', models.TextField(blank=True, null=True, verbose_name='Please provide rationale for the deferred date')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='administrative notes')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csasrequestreview_created_by', to=settings.AUTH_USER_MODEL)),
                ('csas_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='csas2.csasrequest')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='csasrequestreview_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CSASRequestFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=csas2.models.request_directory_path)),
                ('csas_request', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='csas2.csasrequest')),
            ],
            options={
                'ordering': ['-date_created'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='author',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='csas2.document'),
        ),
        migrations.AddField(
            model_name='author',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorship', to='shared_models.person'),
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('document', 'person')},
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='csas2.invitee', verbose_name='attendee')),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('invitee', 'date')},
            },
        ),
    ]