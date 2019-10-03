import datetime
import json
import os
from copy import deepcopy

import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, FormView, TemplateView
from easy_pdf.views import PDFTemplateView
from lib.functions.custom_functions import fiscal_year, listrify
from lib.functions.custom_functions import nz
from . import models
from . import forms
from . import emails
from . import filters
from . import reports
from . import stat_holidays
from shared_models import models as shared_models


def get_help_text_dict():
    my_dict = {}
    for obj in models.HelpText.objects.all():
        my_dict[obj.field_name] = str(obj)

    return my_dict
    #
    # help_text_dict = {
    #     "user": _("This field should be used if the staff member is a DFO employee (as opposed to the 'Person name' field)"),
    #     "start_date": _("This is the start date of the project, not the fiscal year"),
    #     "is_negotiable": _("Is this program a part of DFO's core mandate?"),
    #     "is_competitive": _("For example, is the funding for this project coming from a program like ACRDP, PARR, SPERA, etc.?"),
    #     "priorities": _("What will be the project emphasis in this particular fiscal year?"),
    #     "deliverables": _("Please provide this information in bulleted form, if possible."),
    # }


def in_projects_admin_group(user):
    """
    Will return True if user is in project_admin group
    """
    if user:
        return user.groups.filter(name='projects_admin').count() != 0


def is_management_or_admin(user):
    """
        Will return True if user is in project_admin group, or if user is listed as a head of a section, division or branch
    """
    if user.id:
        if in_projects_admin_group(user) or \
                shared_models.Section.objects.filter(head=user).count() > 0 or \
                shared_models.Division.objects.filter(head=user).count() > 0 or \
                shared_models.Branch.objects.filter(head=user).count() > 0:
            return True


def is_section_head(user, project):
    try:
        return True if project.section.head == user else False
    except AttributeError as e:
        print(e)


def is_division_manager(user, project):
    try:
        return True if project.section.division.head == user else False
    except AttributeError:
        pass


def is_rds(user, project):
    try:
        return True if project.section.division.branch.head == user else False
    except AttributeError:
        pass


def can_modify_project(user, project_id):
    """returns True if user has permissions to delete or modify a project"""
    if user.id:
        project = models.Project.objects.get(pk=project_id)

        # check to see if a superuser or projects_admin -- both are allow to modify projects
        # if user.is_superuser or "projects_admin" in [g.name for g in user.groups.all()]:
        #     return True

        # check to see if they are a project lead
        if user in [staff.user for staff in project.staff_members.filter(lead=True)]:
            return True

        # check to see if they are a section head
        if is_section_head(user, project):
            return True


class ProjectLeadRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        # the assumption is that either we are passing in a Project object or an object that has a project as an attribute
        try:
            obj = self.get_object()
        except AttributeError:
            project_id = self.kwargs.get("project")
        else:
            try:
                project_id = getattr(obj, "project").id
            except AttributeError:
                project_id = obj.id
        finally:
            return can_modify_project(self.request.user, project_id)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))
        return super().dispatch(request, *args, **kwargs)


class ProjectManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        # we need to get the pk for the project. this might be under 1 or 2 kwargs: pk or project
        if self.kwargs.get("pk"):
            project_id = self.kwargs.get("pk")
        else:
            project_id = self.kwargs.get("project")
        project = models.Project.objects.get(pk=project_id)
        if is_section_head(self.request.user, project) or is_division_manager(self.request.user, project) or is_rds(self.request.user,
                                                                                                                    project):
            return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:denied_section_heads_only'))
        return super().dispatch(request, *args, **kwargs)


class ManagerOrAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return is_management_or_admin(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:denied_section_heads_only'))
        return super().dispatch(request, *args, **kwargs)


def financial_summary_data(project):
    salary_abase = 0
    om_abase = 0
    capital_abase = 0

    salary_bbase = 0
    om_bbase = 0
    capital_bbase = 0

    salary_cbase = 0
    om_cbase = 0
    capital_cbase = 0

    gc_total = 0

    # first calc for staff
    for staff in project.staff_members.all():
        # exclude full time employees
        if staff.employee_type.id != 1 or staff.employee_type.id != 6:
            # if the staff member is being paid from bbase...
            if staff.funding_source.id == 1:
                # if salary
                if staff.employee_type.cost_type is 1:
                    salary_abase += nz(staff.cost, 0)
                # if o&M
                elif staff.employee_type.cost_type is 2:
                    om_abase += nz(staff.cost, 0)
            elif staff.funding_source.id == 2:
                # if salary
                if staff.employee_type.cost_type is 1:
                    salary_bbase += nz(staff.cost, 0)
                # if o&M
                elif staff.employee_type.cost_type is 2:
                    om_bbase += nz(staff.cost, 0)
            elif staff.funding_source.id == 3:
                # if salary
                if staff.employee_type.cost_type is 1:
                    salary_cbase += nz(staff.cost, 0)
                # if o&M
                elif staff.employee_type.cost_type is 2:
                    om_cbase += nz(staff.cost, 0)

    # O&M costs
    for cost in project.om_costs.all():
        if cost.funding_source.id == 1:
            om_abase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 2:
            om_bbase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 3:
            om_cbase += nz(cost.budget_requested, 0)

    # Capital costs
    for cost in project.capital_costs.all():
        if cost.funding_source.id == 1:
            capital_abase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 2:
            capital_bbase += nz(cost.budget_requested, 0)
        elif cost.funding_source.id == 3:
            capital_cbase += nz(cost.budget_requested, 0)

    # g&c costs
    for cost in project.gc_costs.all():
        gc_total += nz(cost.budget_requested, 0)

    context = {}
    # abase
    context["salary_abase"] = salary_abase
    context["om_abase"] = om_abase
    context["capital_abase"] = capital_abase

    # bbase
    context["salary_bbase"] = salary_bbase
    context["om_bbase"] = om_bbase
    context["capital_bbase"] = capital_bbase

    # cbase
    context["salary_cbase"] = salary_cbase
    context["om_cbase"] = om_cbase
    context["capital_cbase"] = capital_cbase

    context["salary_total"] = salary_abase + salary_bbase + salary_cbase
    context["om_total"] = om_abase + om_bbase + om_cbase
    context["capital_total"] = capital_abase + capital_bbase + capital_cbase
    context["gc_total"] = gc_total

    # import color schemes from funding_source table
    context["abase"] = models.FundingSource.objects.get(pk=1).color
    context["bbase"] = models.FundingSource.objects.get(pk=2).color
    context["cbase"] = models.FundingSource.objects.get(pk=3).color

    return context


project_field_list = [
    'id',
    'project_title',
    'section',
    'program',
    'programs',
    'tags',
    'responsibility_center',
    'allotment_code',
    'existing_project_code',
    'is_national',
    'is_negotiable',
    'status',
    'is_competitive',
    'is_approved',
    'start_date',
    'end_date',
    'description',
    'priorities',
    'deliverables',
    'data_collection',
    'data_sharing',
    'data_storage',
    'metadata_url',
    'regional_dm',
    'regional_dm_needs',
    'sectional_dm',
    'sectional_dm_needs',
    'vehicle_needs',
    'it_needs',
    'chemical_needs',
    'ship_needs',
    'impacts_if_not_approved',
    'date_last_modified',
    'last_modified_by',
]


def get_section_choices(all=False, full_name=True):
    if full_name:
        my_attr = "full_name"
    else:
        my_attr = _("name")

    return [(s.id, getattr(s, my_attr)) for s in
            shared_models.Section.objects.all().order_by(
                "division__branch__region",
                "division__branch",
                "division",
                "name"
            ) if s.projects.count() > 0] if not all else [(s.id, getattr(s, my_attr)) for s in
                                                          shared_models.Section.objects.filter(
                                                              division__branch__name__icontains="science").order_by(
                                                              "division__branch__region",
                                                              "division__branch",
                                                              "division",
                                                              "name"
                                                          )]


def get_division_choices(all=False):
    if all:
        division_list = set([shared_models.Section.objects.get(pk=s[0]).division for s in get_section_choices(all=True)])
    else:
        division_list = set([shared_models.Section.objects.get(pk=s[0]).division for s in get_section_choices()])
    q_objects = Q()  # Create an empty Q object to start with
    for d in division_list:
        q_objects |= Q(id=d.id)  # 'or' the Q objects together

    return [(d.id, str(d)) for d in
            shared_models.Division.objects.filter(q_objects).order_by(
                "branch__region",
                "name"
            )]


def get_region_choices(all=False):
    if all:
        region_list = set([shared_models.Division.objects.get(pk=d[0]).branch.region for d in get_division_choices(all=True)])
    else:
        region_list = set([shared_models.Division.objects.get(pk=d[0]).branch.region for d in get_division_choices()])
    q_objects = Q()  # Create an empty Q object to start with
    for r in region_list:
        q_objects |= Q(id=r.id)  # 'or' the Q objects together

    return [(r.id, str(r)) for r in
            shared_models.Region.objects.filter(q_objects).order_by(
                "name",
            )]


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'projects/close_me.html'


class IndexTemplateView(TemplateView):
    template_name = 'projects/index.html'


# PROJECTS #
############
class MyProjectListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login_required/'
    template_name = 'projects/my_project_list.html'

    def get_queryset(self):
        return models.Staff.objects.filter(user=self.request.user).order_by("-project__year", "project__project_title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = models.Staff.objects.filter(user=self.request.user)

        # need to produce a dictionary with number of hours committed by fiscal year
        fiscal_year_list = set([p.project.year for p in projects.order_by("project__year_id")])

        weeks_dict = {}
        for fy in fiscal_year_list:
            weeks_dict[fy.id] = {}
            weeks_dict[fy.id]['submitted_approved'] = 0
            weeks_dict[fy.id]['submitted_unapproved'] = 0
            weeks_dict[fy.id]['unsubmitted'] = 0
            weeks_dict[fy.id]['total'] = 0

        for obj in projects.order_by("project__year_id"):
            if obj.project.submitted:
                if obj.project.section_head_approved:
                    weeks_dict[obj.project.year_id]["submitted_approved"] += nz(obj.duration_weeks, 0)
                else:
                    weeks_dict[obj.project.year_id]["submitted_unapproved"] += nz(obj.duration_weeks, 0)
            else:
                weeks_dict[obj.project.year_id]["unsubmitted"] += nz(obj.duration_weeks, 0)
            weeks_dict[obj.project.year_id]["total"] += nz(obj.duration_weeks, 0)

        context["weeks_dict"] = weeks_dict
        context["fy_list"] = fiscal_year_list
        print(weeks_dict)
        return context


class MySectionListView(LoginRequiredMixin, FilterView):
    login_url = '/accounts/login_required/'
    template_name = 'projects/my_section_list.html'
    filterset_class = filters.MySectionFilter

    def get_queryset(self):
        return models.Project.objects.filter(section__head=self.request.user).order_by('-year', 'section__division', 'section',
                                                                                       'project_title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fy_form'] = forms.FYForm(user=self.request.user.id)

        context['type'] = _("section")
        context['next_fiscal_year'] = shared_models.FiscalYear.objects.get(pk=fiscal_year(next=True, sap_style=True))
        context['has_section'] = models.Project.objects.filter(section__head=self.request.user).count() > 0
        return context


class MyDivisionListView(LoginRequiredMixin, FilterView):
    login_url = '/accounts/login_required/'
    template_name = 'projects/my_section_list.html'
    filterset_class = filters.MySectionFilter

    def get_queryset(self):
        return models.Project.objects.filter(section__division__head=self.request.user).order_by('-year', 'section__division', 'section',
                                                                                                 'project_title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = _("division")
        context['fy_form'] = forms.FYForm(user=self.request.user.id)

        context['next_fiscal_year'] = shared_models.FiscalYear.objects.get(pk=fiscal_year(next=True, sap_style=True))
        context['has_section'] = models.Project.objects.filter(section__division__head=self.request.user).count() > 0
        return context


class MyBranchListView(LoginRequiredMixin, FilterView):
    login_url = '/accounts/login_required/'
    template_name = 'projects/my_section_list.html'
    filterset_class = filters.MySectionFilter

    def get_queryset(self):
        return models.Project.objects.filter(section__division__branch__head=self.request.user).order_by('-year', 'section__division',
                                                                                                         'section',
                                                                                                         'project_title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = _("branch")
        context['fy_form'] = forms.FYForm(user=self.request.user.id)
        context['next_fiscal_year'] = shared_models.FiscalYear.objects.get(pk=fiscal_year(next=True, sap_style=True))
        context['has_section'] = models.Project.objects.filter(section__division__branch__head=self.request.user).count() > 0
        return context


class ProjectListView(LoginRequiredMixin, FilterView):
    login_url = '/accounts/login_required/'
    template_name = 'projects/project_list.html'
    queryset = models.Project.objects.filter(is_hidden=False).order_by('-year', 'section__division', 'section', 'project_title')
    filterset_class = filters.ProjectFilter


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = models.Project
    login_url = '/accounts/login_required/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["field_list"] = project_field_list
        context["files"] = project.files.all()

        # bring in financial summary data
        my_context = financial_summary_data(project)
        context = {**my_context, **context}

        # if not can_modify_project(self.request.user, project):
        #     context["report_mode"] = True
        return context


class ProjectPrintDetailView(LoginRequiredMixin, PDFTemplateView):
    model = models.Project
    login_url = '/accounts/login_required/'
    template_name = "projects/project_report.html"

    def get_pdf_filename(self):
        project = models.Project.objects.get(pk=self.kwargs["pk"])
        pdf_filename = "{}-{}-{}-{}-{}.pdf".format(
            project.year.id,
            project.section.division.abbrev,
            project.section.abbrev,
            project.id,
            str(project.project_title).title().replace(" ", "")[:10],
        )

        return pdf_filename

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(pk=self.kwargs["pk"])
        context["report_mode"] = True
        context["object"] = project
        context["field_list"] = project_field_list

        # bring in financial summary data
        my_context = financial_summary_data(project)
        context = {**my_context, **context}

        return context


class ProjectUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context

    def get_initial(self):
        my_dict = {
            'last_modified_by': self.request.user,
        }

        try:
            my_dict["start_date"] = "{}-{:02d}-{:02d}".format(self.object.start_date.year, self.object.start_date.month,
                                                              self.object.start_date.day)
        except:
            print("no start date...")

        try:
            my_dict["end_date"] = "{}-{:02d}-{:02d}".format(self.object.end_date.year, self.object.end_date.month,
                                                            self.object.end_date.day)
        except:
            print("no end date...")

        return my_dict


class ProjectSubmitUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectSubmitForm
    template_name = "projects/project_submit_form.html"

    def get_initial(self):
        if self.object.submitted:
            submit = False
        else:
            submit = True

        return {
            'last_modified_by': self.request.user,
            'submitted': submit,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["field_list"] = project_field_list
        context["report_mode"] = True

        # bring in financial summary data
        my_context = financial_summary_data(project)
        context = {**my_context, **context}

        return context

    def form_valid(self, form):
        my_object = form.save()
        # create a new email object
        email = emails.ProjectSubmissionEmail(self.object)
        # send the email object
        if settings.PRODUCTION_SERVER:
            send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                      recipient_list=email.to_list, fail_silently=False, )
        else:
            print(email)
        messages.success(self.request,
                         _("The project was submitted and an email has been sent to notify the section head!"))
        return super().form_valid(form)


class ProjectApprovalUpdateView(ProjectManagerRequiredMixin, UpdateView):
    model = models.Project
    template_name = "projects/project_approval_form_popout.html"
    success_url = reverse_lazy("projects:close_me")

    def get_form_class(self):
        level = self.kwargs["level"]
        if level == "section":
            return forms.SectionApprovalForm
        elif level == "division":
            return forms.DivisionApprovalForm
        elif level == "branch":
            return forms.BranchApprovalForm

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = models.Project
    login_url = '/accounts/login_required/'
    form_class = forms.NewProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()

        # here are the option objects we want to send in through context
        # only from the science branches of each region

        division_dict = {}
        for d in get_division_choices(all=True):
            my_division = shared_models.Division.objects.get(pk=d[0])
            division_dict[my_division.id] = {}
            division_dict[my_division.id]["display"] = "{} - {}".format(
                getattr(my_division.branch, _("name")),
                getattr(my_division, _("name")),
            )
            division_dict[my_division.id]["region_id"] = my_division.branch.region_id

        section_dict = {}
        for s in get_section_choices(all=True):
            my_section = shared_models.Section.objects.get(pk=s[0])
            section_dict[my_section.id] = {}
            section_dict[my_section.id]["display"] = str(my_section)
            section_dict[my_section.id]["division_id"] = my_section.division_id
        context['division_json'] = json.dumps(division_dict)
        context['section_json'] = json.dumps(section_dict)

        return context

    def form_valid(self, form):
        object = form.save()
        models.Staff.objects.create(project=object, lead=True, employee_type_id=1, user_id=self.request.user.id)

        for obj in models.OMCategory.objects.all():
            new_item = models.OMCost.objects.create(project=object, om_category=obj)
            new_item.save()

        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": object.id}))

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ProjectDeleteView(ProjectLeadRequiredMixin, DeleteView):
    model = models.Project
    success_url = reverse_lazy('projects:my_project_list')
    success_message = _('The project was successfully deleted!')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ProjectCloneUpdateView(ProjectUpdateView):
    def test_func(self):
        if self.request.user.id:
            return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:denied_access'))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        my_object = models.Project.objects.get(pk=self.kwargs["pk"])
        init = super().get_initial()
        init["project_title"] = "CLONE OF: {}".format(my_object.project_title)
        init["year"] = fiscal_year(sap_style=True, next=True)
        # init["created_by"] = self.request.user
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.Project.objects.get(pk=new_obj.pk)
        new_obj.pk = None
        new_obj.submitted = False
        new_obj.section_head_approved = False
        new_obj.section_head_feedback = None
        new_obj.manager_approved = False
        new_obj.manager_feedback = None
        new_obj.rds_approved = False
        new_obj.rds_feedback = None
        new_obj.date_last_modified = timezone.now()
        new_obj.last_modified_by = self.request.user
        new_obj.save()

        # Now we need to replicate all the related records:
        # 1) staff
        for old_rel_obj in old_obj.staff_members.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project = new_obj
            new_rel_obj.save()

        # we have to just make sure that the user is a lead on the project. Otherwise they will not be able to edit.
        my_staff, created = models.Staff.objects.get_or_create(
            user=self.request.user,
            project=new_obj,
            employee_type_id=1,
        )
        my_staff.lead = True
        my_staff.save()

        # 2) O&M
        for old_rel_obj in old_obj.om_costs.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project = new_obj
            new_rel_obj.save()

        # 3) Capital
        for old_rel_obj in old_obj.capital_costs.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project = new_obj
            new_rel_obj.save()

        # 4) G&C
        for old_rel_obj in old_obj.gc_costs.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project = new_obj
            new_rel_obj.save()

        # 5) Collaborators and Partners
        for old_rel_obj in old_obj.collaborators.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project = new_obj
            new_rel_obj.save()

        # 6) Collaborative Agreements
        for old_rel_obj in old_obj.agreements.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project = new_obj
            new_rel_obj.save()

        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": new_obj.id}))


# STAFF #
#########

class StaffCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.Staff
    template_name = 'projects/staff_form_popout.html'
    form_class = forms.StaffForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        context['help_text_dict'] = get_help_text_dict()
        return context

    def form_valid(self, form):
        object = form.save()
        if form.cleaned_data["save_then_go_OT"] == "1":
            return HttpResponseRedirect(reverse_lazy('projects:ot_calc', kwargs={"pk": object.id}))
        else:
            return HttpResponseRedirect(reverse('projects:close_me'))


class StaffUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.Staff
    template_name = 'projects/staff_form_popout.html'
    form_class = forms.StaffForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context


def staff_delete(request, pk):
    object = models.Staff.objects.get(pk=pk)

    if can_modify_project(request.user, object.project.id):
        object.delete()
        messages.success(request, _("The staff member has been successfully deleted from project."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": object.project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


class OverTimeCalculatorTemplateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login_required/'
    template_name = 'projects/overtime_calculator_popout.html'
    form_class = forms.OTForm
    model = models.Staff

    def get_initial(self):
        return {
            # 'weekdays': 0,
            # 'saturdays': 0,
            # 'sundays': 0,
            # 'stat_holidays': 0,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # send in the upcoming fiscal year string
        context["next_fiscal_year"] = fiscal_year(next=True)

        # create a pandas date_range object for upcoming fiscal year
        target_year = fiscal_year(next=True, sap_style=True)
        start = "{}-04-01".format(target_year - 1)
        end = "{}-03-31".format(target_year)
        datelist = pd.date_range(start=start, end=end).tolist()
        context['datelist'] = datelist

        # send in a list of stat holidays
        context["stat_holiday_list"] = stat_holidays.stat_holiday_list
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy('projects:staff_edit', kwargs={"pk": object.id}))


# this is a temp view DJF created to walkover the `program` field to the new `programs` field
@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def temp_formset(request):
    context = {}
    # if the formset is being submitted
    if request.method == 'POST':
        # choose the appropriate formset based on the `extra` arg
        formset = forms.TempFormSet(request.POST)

        if formset.is_valid():
            formset.save()
            # pass the specimen through the make_flags helper function to assign any QC flags

            # redirect back to the observation_formset with the blind intention of getting another observation
            return HttpResponseRedirect(reverse("projects:formset"))
    # otherwise the formset is just being displayed
    else:
        # prep the formset...for display
        formset = forms.TempFormSet(
            queryset=models.Project.objects.filter(section__division__branch__region__id=2).order_by("program")
        )
    context['formset'] = formset
    context['my_object'] = models.Project.objects.first()
    context['field_list'] = [
        'project_title',
        'program',
        'programs',
        'tags',
    ]
    return render(request, 'projects/temp_formset.html', context)


# this is a temp view DJF created to walkover the `program` field to the new `programs` field
class MyTempListView(LoginRequiredMixin, ListView):
    queryset = models.Project.objects.filter(section__division__branch__region__id=2).order_by(
        "section__division__branch__region",
        "section__division",
        "section",
        "program",
    )
    template_name = 'projects/my_temp_list.html'


# COLLABORATOR #
################

class CollaboratorCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.Collaborator
    template_name = 'projects/collaborator_form_popout.html'
    form_class = forms.CollaboratorForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


class CollaboratorUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.Collaborator
    template_name = 'projects/collaborator_form_popout.html'
    form_class = forms.CollaboratorForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


def collaborator_delete(request, pk):
    object = models.Collaborator.objects.get(pk=pk)
    if can_modify_project(request.user, object.project.id):
        object.delete()
        messages.success(request, _("The collaborator has been successfully deleted from project."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": object.project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


# AGREEMENTS #
##############

class AgreementCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.CollaborativeAgreement
    template_name = 'projects/agreement_form_popout.html'
    form_class = forms.AgreementForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


class AgreementUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.CollaborativeAgreement
    template_name = 'projects/agreement_form_popout.html'
    form_class = forms.AgreementForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


def agreement_delete(request, pk):
    object = models.CollaborativeAgreement.objects.get(pk=pk)
    if can_modify_project(request.user, object.project.id):
        object.delete()
        messages.success(request, _("The agreement has been successfully deleted."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": object.project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


# OM COSTS #
############

class OMCostCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.OMCost
    template_name = 'projects/cost_form_popout.html'
    form_class = forms.OMCostForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        context['cost_type'] = "O&M"
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


class OMCostUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.OMCost
    template_name = 'projects/cost_form_popout.html'
    form_class = forms.OMCostForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost_type'] = _("O&M")
        return context


def om_cost_delete(request, pk):
    object = models.OMCost.objects.get(pk=pk)
    if can_modify_project(request.user, object.project.id):
        object.delete()
        messages.success(request, _("The cost has been successfully deleted."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": object.project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


def om_cost_clear(request, project):
    project = models.Project.objects.get(pk=project)
    if can_modify_project(request.user, project.id):
        for obj in models.OMCategory.objects.all():
            for cost in models.OMCost.objects.filter(project=project, om_category=obj):
                print(cost)
                if (cost.budget_requested is None or cost.budget_requested == 0) and not cost.description:
                    cost.delete()

        messages.success(request, _("All empty O&M lines have been cleared."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


def om_cost_populate(request, project):
    project = models.Project.objects.get(pk=project)
    if can_modify_project(request.user, project.id):
        for obj in models.OMCategory.objects.all():
            if not models.OMCost.objects.filter(project=project, om_category=obj).count():
                new_item = models.OMCost.objects.create(project=project, om_category=obj)
                new_item.save()

        messages.success(request, _("All O&M categories have been added to this project."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


# CAPITAL COSTS #
#################

class CapitalCostCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.CapitalCost
    template_name = 'projects/cost_form_popout.html'
    form_class = forms.CapitalCostForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        context['cost_type'] = "Capital"
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


class CapitalCostUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.CapitalCost
    template_name = 'projects/cost_form_popout.html'
    form_class = forms.CapitalCostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost_type'] = "Capital"
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


def capital_cost_delete(request, pk):
    object = models.CapitalCost.objects.get(pk=pk)
    if can_modify_project(request.user, object.project.id):
        object.delete()
        messages.success(request, _("The cost has been successfully deleted."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": object.project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


# GC COSTS #
############

class GCCostCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.GCCost
    template_name = 'projects/cost_form_popout.html'
    form_class = forms.GCCostForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        context['cost_type'] = "G&C"
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


class GCCostUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.GCCost
    template_name = 'projects/cost_form_popout.html'
    form_class = forms.GCCostForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost_type'] = "G&C"
        return context


def gc_cost_delete(request, pk):
    object = models.GCCost.objects.get(pk=pk)
    if can_modify_project(request.user, object.project.id):
        object.delete()
        messages.success(request, _("The cost has been successfully deleted."))
        return HttpResponseRedirect(reverse_lazy("projects:project_detail", kwargs={"pk": object.project.id}))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


# SHARED #
##########
def toggle_source(request, pk, type):
    if type == "om":
        my_cost = models.OMCost.objects.get(pk=pk)
    elif type == "capital":
        my_cost = models.CapitalCost.objects.get(pk=pk)
    elif type == "staff":
        my_cost = models.Staff.objects.get(pk=pk)
    # otherwise function is being used improperly
    if can_modify_project(request.user, my_cost.project.id):
        if my_cost.funding_source_id is None:
            my_cost.funding_source_id = 1
        elif my_cost.funding_source_id == 1:
            my_cost.funding_source_id = 2
        elif my_cost.funding_source_id == 2:
            my_cost.funding_source_id = 3
        else:
            my_cost.funding_source_id = 1
        my_cost.save()

        return HttpResponseRedirect(
            reverse_lazy("projects:project_detail", kwargs={"pk": my_cost.project.id}) + "?#{}-{}".format(type, pk))
    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


# FILES #
#########

class FileCreateView(ProjectLeadRequiredMixin, CreateView):
    template_name = "projects/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse("shared_models:close_me"))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        project = models.Project.objects.get(pk=self.kwargs['project'])
        context["project"] = project
        return context

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        status_report = models.StatusReport.objects.get(pk=self.kwargs['status_report']) if self.kwargs.get('status_report') else None

        return {
            'project': project,
            'status_report': status_report,
        }


class FileUpdateView(ProjectLeadRequiredMixin, UpdateView):
    template_name = "projects/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("projects:file_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context


class FileDetailView(FileUpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context


class FileDeleteView(ProjectLeadRequiredMixin, DeleteView):
    template_name = "projects/file_confirm_delete.html"
    model = models.File

    def get_success_url(self, **kwargs):
        return reverse_lazy("shared_models:close_me")


# REPORTS #
###########

class ReportSearchFormView(ManagerOrAdminRequiredMixin, FormView):
    template_name = 'projects/report_search.html'
    form_class = forms.ReportSearchForm

    # def get_initial(self):
    # default the year to the year of the latest samples
    # return {"fiscal_year": fiscal_year(next=True, sap_style=True)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        division_dict = {}
        for d in get_division_choices():
            my_division = shared_models.Division.objects.get(pk=d[0])
            division_dict[my_division.id] = {}
            division_dict[my_division.id]["display"] = getattr(my_division, _("name"))
            division_dict[my_division.id]["region_id"] = my_division.branch.region_id

        section_dict = {}
        for s in get_section_choices():
            my_section = shared_models.Section.objects.get(pk=s[0])
            section_dict[my_section.id] = {}
            section_dict[my_section.id]["display"] = str(my_section)
            section_dict[my_section.id]["division_id"] = my_section.division_id

        context['division_json'] = json.dumps(division_dict)
        context['section_json'] = json.dumps(section_dict)
        return context

    def form_valid(self, form):
        fiscal_year = str(form.cleaned_data["fiscal_year"])
        report = int(form.cleaned_data["report"])
        regions = listrify(form.cleaned_data["region"])
        divisions = listrify(form.cleaned_data["division"])
        sections = listrify(form.cleaned_data["section"])

        if regions == "":
            regions = "None"
        if divisions == "":
            divisions = "None"
        if sections == "":
            sections = "None"

        if report == 1:
            return HttpResponseRedirect(reverse("projects:report_master", kwargs={
                'fiscal_year': fiscal_year,
                'regions': regions,
                'divisions': divisions,
                'sections': sections,
            }))
        elif report == 2:
            return HttpResponseRedirect(reverse("projects:pdf_printout", kwargs={
                'fiscal_year': fiscal_year,
                'regions': regions,
                'divisions': divisions,
                'sections': sections,
            }))
        elif report == 3:
            return HttpResponseRedirect(reverse("projects:pdf_project_summary", kwargs={
                'fiscal_year': fiscal_year,
                'regions': regions,
                'divisions': divisions,
                'sections': sections,
            }))
        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("projects:report_search"))


def master_spreadsheet(request, fiscal_year, regions=None, divisions=None, sections=None, user=None):
    # sections arg will be coming in as None from the my_section view
    if regions is None:
        regions = "None"
    if divisions is None:
        divisions = "None"
    if sections is None:
        sections = "None"
    file_url = reports.generate_master_spreadsheet(fiscal_year, regions, divisions, sections, user)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="Science project planning MASTER LIST {}.xlsx"'.format(
                fiscal_year)
            return response
    raise Http404


class PDFProjectSummaryReport(LoginRequiredMixin, PDFTemplateView):
    login_url = '/accounts/login_required/'
    template_name = "projects/report_pdf_project_summary.html"

    def get_pdf_filename(self):
        fy = shared_models.FiscalYear.objects.get(pk=self.kwargs["fiscal_year"])
        pdf_filename = "{} Project Summary Report.pdf".format(fy)
        return pdf_filename

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fy = shared_models.FiscalYear.objects.get(pk=self.kwargs["fiscal_year"])

        # need to assemble a section list
        ## first look at the sections arg; if not null, we don't need anything else
        if self.kwargs["sections"] != "None":
            section_list = shared_models.Section.objects.filter(id__in=self.kwargs["sections"].split(","))
        ## next look at the divisions arg; if not null, we don't need anything else
        elif self.kwargs["divisions"] != "None":
            section_list = shared_models.Section.objects.filter(division_id__in=self.kwargs["divisions"].split(","))
        ## next look at the divisions arg; if not null, we don't need anything else
        elif self.kwargs["regions"] != "None":
            section_list = shared_models.Section.objects.filter(division__branch__region_id__in=self.kwargs["regions"].split(","))
        else:
            section_list = []

        project_list = models.Project.objects.filter(year=fy, submitted=True, section_head_approved=True,
                                                     section_id__in=section_list).order_by("id")

        context["fy"] = fy
        context["report_mode"] = True
        context["object_list"] = project_list
        context["field_list"] = project_field_list
        context["division_list"] = [shared_models.Division.objects.get(pk=item["section__division"]) for item in
                                    project_list.values("section__division").order_by("section__division").distinct()]
        # bring in financial summary data for each project:
        context["financial_summary_data"] = {}
        context["financial_summary_data"]["sections"] = {}
        context["financial_summary_data"]["divisions"] = {}
        key_list = [
            "salary_abase",
            "salary_bbase",
            "salary_cbase",
            "om_abase",
            "om_bbase",
            "om_cbase",
            "capital_abase",
            "capital_bbase",
            "capital_cbase",
            "salary_total",
            "om_total",
            "capital_total",
            "students",
            "casuals",
            "OT",
        ]

        for project in project_list:
            context["financial_summary_data"][project.id] = financial_summary_data(project)
            context["financial_summary_data"][project.id]["students"] = project.staff_members.filter(employee_type=4).count()
            context["financial_summary_data"][project.id]["casuals"] = project.staff_members.filter(employee_type=3).count()
            context["financial_summary_data"][project.id]["OT"] = nz(project.staff_members.values("overtime_hours").order_by(
                "overtime_hours").aggregate(dsum=Sum("overtime_hours"))["dsum"], 0)

            # for sections
            try:
                context["financial_summary_data"]["sections"][project.section.id]
            except KeyError:
                context["financial_summary_data"]["sections"][project.section.id] = {}
                # go through the keys and make sure each category is initialized
                for key in key_list:
                    context["financial_summary_data"]["sections"][project.section.id][key] = 0
            finally:
                for key in key_list:
                    context["financial_summary_data"]["sections"][project.section.id][key] += context["financial_summary_data"][project.id][
                        key]

            # for Divisions
            try:
                context["financial_summary_data"]["divisions"][project.section.division.id]
            except KeyError:
                context["financial_summary_data"]["divisions"][project.section.division.id] = {}
                # go through the keys and make sure each category is initialized
                for key in key_list:
                    context["financial_summary_data"]["divisions"][project.section.division.id][key] = 0
            finally:
                for key in key_list:
                    context["financial_summary_data"]["divisions"][project.section.division.id][key] += \
                        context["financial_summary_data"][project.id][key]

            # for total
            try:
                context["financial_summary_data"]["total"]
            except KeyError:
                context["financial_summary_data"]["total"] = {}
                # go through the keys and make sure each category is initialized
                for key in key_list:
                    context["financial_summary_data"]["total"][key] = 0
            finally:
                for key in key_list:
                    context["financial_summary_data"]["total"][key] += \
                        context["financial_summary_data"][project.id][key]

        # get a list of the capital requests
        context["capital_list"] = [capital_cost for project in project_list for capital_cost in project.capital_costs.all()]

        # get a list of the G&Cs
        context["gc_list"] = [gc for project in project_list for gc in project.gc_costs.all()]

        # get a list of the collaborators
        context["collaborator_list"] = [collaborator for project in project_list for collaborator in project.collaborators.all()]

        # get a list of the agreements
        context["agreement_list"] = [agreement for project in project_list for agreement in project.agreements.all()]

        return context


class PDFProjectPrintoutReport(LoginRequiredMixin, PDFTemplateView):
    login_url = '/accounts/login_required/'
    template_name = "projects/report_pdf_printout.html"

    def get_pdf_filename(self):
        fy = shared_models.FiscalYear.objects.get(pk=self.kwargs["fiscal_year"])
        pdf_filename = "{} Workplan Export.pdf".format(fy)
        return pdf_filename

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fy = shared_models.FiscalYear.objects.get(pk=self.kwargs["fiscal_year"])

        # need to assemble a section list
        ## first look at the sections arg; if not null, we don't need anything else
        if self.kwargs["sections"] != "None":
            section_list = shared_models.Section.objects.filter(id__in=self.kwargs["sections"].split(","))
        ## next look at the divisions arg; if not null, we don't need anything else
        elif self.kwargs["divisions"] != "None":
            section_list = shared_models.Section.objects.filter(division_id__in=self.kwargs["divisions"].split(","))
        ## next look at the divisions arg; if not null, we don't need anything else
        elif self.kwargs["regions"] != "None":
            section_list = shared_models.Section.objects.filter(division__branch__region_id__in=self.kwargs["regions"].split(","))
        else:
            section_list = []

        project_list = models.Project.objects.filter(year=fy, submitted=True, section_head_approved=True,
                                                     section_id__in=section_list).order_by("id")

        # project_list = [project for project in project_list if project.section in section_list]

        context["fy"] = fy
        context["report_mode"] = True
        context["object_list"] = project_list
        context["field_list"] = project_field_list
        context["division_list"] = set([s.division for s in section_list])
        # bring in financial summary data for each project:
        context["financial_summary_data"] = {}
        context["financial_summary_data"]["sections"] = {}
        context["financial_summary_data"]["divisions"] = {}
        key_list = [
            "salary_abase",
            "salary_bbase",
            "salary_cbase",
            "om_abase",
            "om_bbase",
            "om_cbase",
            "capital_abase",
            "capital_bbase",
            "capital_cbase",
            "students",
            "casuals",
            "OT",
        ]

        for project in project_list:
            context["financial_summary_data"][project.id] = financial_summary_data(project)

        return context


def workplan_summary(request, fiscal_year):
    file_url = reports.generate_workplan_summary(fiscal_year)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="{} Workplan Summary.xlsx"'.format(
                fiscal_year)
            return response
    raise Http404


# USER #
########

# this is a complicated cookie. Therefore we will not use a model view or model form and handle the clean data manually.
class UserCreateView(LoginRequiredMixin, FormView):
    form_class = forms.UserCreateForm
    template_name = 'projects/user_form.html'
    login_url = '/accounts/login_required/'

    def get_success_url(self):
        return reverse_lazy('projects:close_me')

    def form_valid(self, form):
        # retrieve data from form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email1']

        # create a new user
        User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
            is_active=1,
            email=email,
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# SETTINGS #
############

@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_funding_source(request, pk):
    my_obj = models.FundingSource.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_funding_sources"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_funding_sources(request):
    qs = models.FundingSource.objects.all()
    if request.method == 'POST':
        formset = forms.FundingSourceFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_funding_sources"))
    else:
        formset = forms.FundingSourceFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
        'color',
    ]
    context['title'] = "Manage Funding Sources"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_om_cat(request, pk):
    my_obj = models.OMCategory.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_om_cats"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_om_cats(request):
    qs = models.OMCategory.objects.all()
    if request.method == 'POST':
        formset = forms.OMCategoryFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_om_cats"))
    else:
        formset = forms.OMCategoryFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
        'group',
    ]
    context['title'] = "Manage O & M Categories"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_employee_type(request, pk):
    my_obj = models.EmployeeType.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_om_cats"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_employee_types(request):
    qs = models.EmployeeType.objects.all()
    if request.method == 'POST':
        formset = forms.EmployeeTypeFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_om_cats"))
    else:
        formset = forms.EmployeeTypeFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
        'cost_type',
        'exclude_from_rollup',
    ]
    context['title'] = "Manage Employee Types"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_status(request, pk):
    my_obj = models.Status.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_statuses"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_statuses(request):
    qs = models.Status.objects.all()
    if request.method == 'POST':
        formset = forms.StatusFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_statuses"))
    else:
        formset = forms.StatusFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'used_for',
        'name',
        'nom',
        'order',
        'color',
    ]
    context['title'] = "Manage Statuses"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_tag(request, pk):
    my_obj = models.Tag.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_tags"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_tags(request):
    qs = models.Tag.objects.all()
    if request.method == 'POST':
        formset = forms.TagFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_tags"))
    else:
        formset = forms.TagFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
        'nom',
    ]
    context['title'] = "Manage Tags"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_help_text(request, pk):
    my_obj = models.HelpText.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_tags"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_help_text(request):
    qs = models.HelpText.objects.all()
    if request.method == 'POST':
        formset = forms.HelpTextFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_help_text"))
    else:
        formset = forms.HelpTextFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'field_name',
        'eng_text',
        'fra_text',
    ]
    context['title'] = "Manage Help Text"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_level(request, pk):
    my_obj = models.Level.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_levels"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_levels(request):
    qs = models.Level.objects.all()
    if request.method == 'POST':
        formset = forms.LevelFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_levels"))
    else:
        formset = forms.LevelFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'name',
    ]
    context['title'] = "Manage Levels"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def delete_program(request, pk):
    my_obj = models.Program2.objects.get(pk=pk)
    my_obj.delete()
    return HttpResponseRedirect(reverse("projects:manage_programs"))


@login_required(login_url='/accounts/login_required/')
@user_passes_test(in_projects_admin_group, login_url='/accounts/denied/')
def manage_programs(request):
    qs = models.Program2.objects.all()
    if request.method == 'POST':
        formset = forms.ProgramFormSet(request.POST, )
        if formset.is_valid():
            formset.save()
            # do something with the formset.cleaned_data
            messages.success(request, "Items have been successfully updated")
            return HttpResponseRedirect(reverse("projects:manage_programs"))
    else:
        formset = forms.ProgramFormSet(
            queryset=qs)
    context = {}
    context["my_object"] = qs.first()
    context["field_list"] = [
        'national_responsibility_eng',
        'national_responsibility_fra',
        'program_inventory',
        'funding_source_and_type',
        'regional_program_name_eng',
        'regional_program_name_fra',
        'examples',
    ]
    context['title'] = "Manage Programs"
    context['formset'] = formset
    return render(request, 'projects/manage_settings_small.html', context)


# STATUS REPORT #
#################

class StatusReportCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.StatusReport
    template_name = 'projects/status_report_form_popout.html'
    form_class = forms.StatusReportForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
            'created_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        context['status_report'] = True
        context['files'] = project.files.filter(reference=2)
        return context

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy('projects:report_edit', kwargs={"pk": my_object.id}))


class StatusReportUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.StatusReport
    template_name = 'projects/status_report_form_popout.html'

    # form_class = forms.StatusReportForm

    def get_form_class(self):
        my_project = self.get_object().project
        if is_section_head(self.request.user, my_project):
            print(123)
            return forms.StatusReportSectionHeadForm
        else:
            print(321)
            return forms.StatusReportForm

    def get_initial(self):
        return {'created_by': self.request.user, }

    def dispatch(self, request, *args, **kwargs):
        # when the view loads, let's make sure that all the milestones are on the project.
        my_object = self.get_object()
        my_project = my_object.project
        for milestone in my_project.milestones.all():
            my_update, created = models.MilestoneUpdate.objects.get_or_create(
                milestone=milestone,
                status_report=my_object
            )
            # if the update is being created, what should be the starting status?
            # to know, we would have to look and see if there is another report. if there is, we should grab the penultimate report and copy status from there.
            if created:
                # check to see if there is another update on the same milestone. We can do this since milestones are unique to projects.
                if milestone.updates.count() > 1:
                    # if there are more than just 1 (i.e. the one we just created), it will be the second record we are interested in...
                    last_update = milestone.updates.all()[1]
                    my_update.status = last_update.status
                    my_update.save()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context["object"].project
        context['status_report'] = self.get_object()
        context['project'] = project
        context['files'] = self.get_object().files.all()
        return context

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse_lazy('projects:report_edit', kwargs={"pk": my_object.id}))


class StatusReportDeleteView(ProjectLeadRequiredMixin, DeleteView):
    template_name = "projects/status_report_confirm_delete.html"
    model = models.StatusReport

    def get_success_url(self, **kwargs):
        return reverse_lazy("shared_models:close_me")


class StatusReportPrintDetailView(LoginRequiredMixin, PDFTemplateView):
    model = models.Project
    login_url = '/accounts/login_required/'
    template_name = "projects/status_report_pdf.html"

    def get_pdf_filename(self):
        my_report = models.StatusReport.objects.get(pk=self.kwargs["pk"])
        pdf_filename = "{}.pdf".format(
            my_report
        )
        return pdf_filename

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_report = models.StatusReport.objects.get(pk=self.kwargs["pk"])
        context["object"] = my_report
        context["report_mode"] = True
        context['files'] = my_report.files.all()

        context["field_list"] = [
            'date_created',
            'created_by',
            'status',
            'major_accomplishments',
            'major_issues',
            'target_completion_date',
            'rationale_for_modified_completion_date',
            'general_comment',
            'section_head_comment',
            'section_head_reviewed',
        ]

        return context


# MILESTONE #
#############

class MilestoneCreateView(ProjectLeadRequiredMixin, CreateView):
    model = models.Milestone
    template_name = 'projects/milestone_form_popout.html'
    form_class = forms.MilestoneForm

    def get_initial(self):
        project = models.Project.objects.get(pk=self.kwargs['project'])
        return {
            'project': project,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = models.Project.objects.get(id=self.kwargs['project'])
        context['project'] = project
        # context['cost_type'] = "G&C"
        return context

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))


class MilestoneUpdateView(ProjectLeadRequiredMixin, UpdateView):
    model = models.Milestone
    template_name = 'projects/milestone_form_popout.html'
    form_class = forms.MilestoneForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = context["object"].project
        return context


def milestone_delete(request, pk):
    object = models.Milestone.objects.get(pk=pk)
    if can_modify_project(request.user, object.project.id):
        object.delete()
        messages.success(request, _("The milestone has been successfully deleted."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(reverse('accounts:denied_project_leads_only'))


# MILESTONE UPDATE #
####################

class MilestoneUpdateUpdateView(UpdateView):
    model = models.MilestoneUpdate
    template_name = 'projects/milestone_form_popout.html'
    form_class = forms.MilestoneUpdateForm

    def form_valid(self, form):
        my_object = form.save()
        return HttpResponseRedirect(reverse('projects:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['project'] = context["object"].project
        return context
