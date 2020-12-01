import json
from copy import deepcopy

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _, gettext_lazy

from shared_models import models as shared_models
from shared_models.views import CommonTemplateView, CommonCreateView, \
    CommonDetailView, CommonFilterView, CommonDeleteView, CommonUpdateView, CommonListView, CommonHardDeleteView, CommonFormsetView
from . import filters
from . import forms
from . import models
from .mixins import CanModifyProjectRequiredMixin, AdminRequiredMixin, ProjectLeadRequiredMixin
from .utils import get_help_text_dict, \
    get_division_choices, get_section_choices, get_project_field_list, get_project_year_field_list, is_management_or_admin, \
    get_review_score_rubric, get_status_report_field_list


class IndexTemplateView(LoginRequiredMixin, CommonTemplateView):
    template_name = 'projects2/index.html'
    h1 = gettext_lazy("DFO Science Project Planning")
    active_page_name_crumb = gettext_lazy("Home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section_id_list = []
        if self.request.user.id:
            if self.request.user.groups.filter(name="projects_admin").count() > 0:
                section_id_list = [project.section_id for project in models.Project.objects.all()]
                section_list = shared_models.Section.objects.filter(id__in=section_id_list)
            else:
                pass
        context["is_management_or_admin"] = is_management_or_admin(self.request.user)
        context["reference_materials"] = models.ReferenceMaterial.objects.all()
        context["upcoming_dates"] = models.UpcomingDate.objects.filter(date__gte=timezone.now()).order_by("date")
        context["past_dates"] = models.UpcomingDate.objects.filter(date__lt=timezone.now()).order_by("date")
        context["upcoming_dates_field_list"] = [
            "date",
            "region",
            "tdescription|{}".format("description"),
        ]
        return context


# PROJECTS #
############


class ExploreProjectsTemplateView(LoginRequiredMixin, CommonTemplateView):
    h1 = gettext_lazy("Projects")
    template_name = 'projects2/explore_projects/main.html'
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"
    subtitle = gettext_lazy("Explore Projects")
    field_list = [
        'id',
        'title',
        'fiscal year',
        'status',
        # 'section',
        'default_funding_source',
        'functional_group',
        'lead_staff',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_project"] = models.Project.objects.first()
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in models.ProjectYear.status_choices]
        return context


class ManageProjectsTemplateView(LoginRequiredMixin, CommonTemplateView):
    h1 = gettext_lazy("Projects")
    template_name = 'projects2/manage_projects/main.html'
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"
    subtitle = gettext_lazy("Manage Projects")
    field_list = [
        'id',
        'fiscal year',
        'title',
        # 'section',
        'default_funding_source',
        'functional_group',
        'lead_staff',
        'status',
        'allocated_budget',
        'review_score_percentage',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_project"] = models.Project.objects.first()
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in models.ProjectYear.status_choices]
        context["review_form"] = forms.ReviewForm
        context["approval_form"] = forms.ApprovalForm
        context["review_score_rubric"] = json.dumps(get_review_score_rubric())
        return context


class MyProjectListView(LoginRequiredMixin, CommonListView):
    template_name = 'projects2/my_project_list.html'
    # filterset_class = filters.MyProjectFilter
    h1 = gettext_lazy("My projects")
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"
    row_object_url_name = "projects2:project_detail"
    new_object_url = reverse_lazy("projects2:project_new")
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'section', "class": "", "width": ""},
        {"name": 'title', "class": "", "width": ""},
        {"name": 'start_date', "class": "", "width": "150px"},
        {"name": 'lead_staff', "class": "", "width": ""},
        {"name": 'fiscal_years', "class": "", "width": ""},
        {"name": 'has_unsubmitted_years|{}'.format("has unsubmitted years?"), "class": "", "width": ""},
        {"name": 'is_hidden|{}'.format(_("hidden?")), "class": "", "width": ""},
        {"name": 'updated_at', "class": "", "width": "150px"},
    ]

    # x = [
    #     "recommended_for_funding",
    #     "approved",
    #     "status_report|{}".format("Status reports"),
    # ]

    def get_queryset(self):
        project_ids = [staff.project_year.project_id for staff in self.request.user.staff_instances2.all()]
        return models.Project.objects.filter(id__in=project_ids).order_by("-updated_at", "title")

    # def get_filterset_kwargs(self, filterset_class):
    #     kwargs = super().get_filterset_kwargs(filterset_class)
    #     if kwargs["data"] is None:
    #         kwargs["data"] = {"year": fiscal_year(next=True, sap_style=True)}
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my"] = True
        # # Based on the default sorting order, we get the fiscal year from the first project instance
        # object_list = context.get("object_list")  # grab the projects returned by the filter
        # fy = object_list.first().year if object_list.count() > 0 else None
        #
        # staff_instances = self.request.user.staff_instances2.filter(project__year=fy)
        #
        # context['fte_approved_projects'] = staff_instances.filter(
        #     project__recommended_for_funding=True, project__submitted=True
        # ).aggregate(dsum=Sum("duration_weeks"))["dsum"]
        #
        # context['fte_unapproved_projects'] = staff_instances.filter(
        #     project__recommended_for_funding=False, project__submitted=True
        # ).aggregate(dsum=Sum("duration_weeks"))["dsum"]
        #
        # context['fte_unsubmitted_projects'] = staff_instances.filter(
        #     project__submitted=False
        # ).aggregate(dsum=Sum("duration_weeks"))["dsum"]
        #
        # context['fy'] = fy
        #
        # context["project_list"] = models.Project.objects.filter(
        #     id__in=[s.project.id for s in self.request.user.staff_instances.all()]
        # )
        #
        # context["project_field_list"] = [
        #     "year",
        #     "submitted|{}".format("Submitted"),
        #     "recommended_for_funding",
        #     "approved",
        #     "allocated_budget",
        #     "section|Section",
        #     "project_title",
        #     "is_hidden|is this a hidden project?",
        #     "is_lead|{}?".format("Are you a project lead"),
        #     "status_report|{}".format("Status reports"),
        # ]

        return context


class ProjectCreateView(LoginRequiredMixin, CommonCreateView):
    model = models.Project
    form_class = forms.NewProjectForm
    home_url_name = "projects2:index"
    template_name = 'projects2/project_form.html'
    container_class = "container bg-light curvy"

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
        my_object = form.save(commit=False)
        # modifications to project instance before saving
        my_object.modified_by = self.request.user
        my_object.save()
        #
        # # create a first year of the project
        # year = models.ProjectYear.objects.create(
        #     project=my_object,
        # )
        # # populate some initial staff and om costs
        # models.Staff.objects.create(
        #     project_year=year,
        #     is_lead=True,
        #     employee_type_id=1,
        #     user_id=self.request.user.id,
        #     funding_source=my_object.default_funding_source
        # )
        # year.add_all_om_costs()
        messages.success(self.request,
                         mark_safe(_("Your new project was created successfully! To get started, <b>add a new project year</b>.")))
        return HttpResponseRedirect(reverse_lazy("projects2:project_detail", kwargs={"pk": my_object.id}))

    def get_initial(self):
        return {'last_modified_by': self.request.user}


class ProjectDetailView(LoginRequiredMixin, CommonDetailView):
    model = models.Project
    template_name = 'projects2/project_detail/project_detail.html'
    home_url_name = "projects2:index"
    container_class = "container-fluid bg-light curvy"

    # parent_crumb = {"title": _("My Projects"), "url": reverse_lazy("projects2:my_project_list")}

    def get_active_page_name_crumb(self):
        return str(self.get_object())

    def get_h1(self):
        mystr = str(self.get_object())
        return mystr

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # If this is a gulf region project, only show the gulf region fields
        context["project_field_list"] = get_project_field_list(project)
        context["project_year_field_list"] = get_project_year_field_list()

        context["staff_form"] = forms.StaffForm
        context["random_staff"] = models.Staff.objects.first()

        context["om_cost_form"] = forms.OMCostForm
        context["random_om_cost"] = models.OMCost.objects.first()

        context["capital_cost_form"] = forms.CapitalCostForm
        context["random_capital_cost"] = models.CapitalCost.objects.first()

        context["gc_cost_form"] = forms.GCCostForm
        context["random_gc_cost"] = models.GCCost.objects.first()

        context["milestone_form"] = forms.MilestoneForm
        context["random_milestone"] = models.Milestone.objects.first()

        context["collaborator_form"] = forms.CollaboratorForm
        context["random_collaborator"] = models.Collaborator.objects.first()

        context["agreement_form"] = forms.AgreementForm
        context["random_agreement"] = models.CollaborativeAgreement.objects.first()

        context["status_report_form"] = forms.StatusReportForm(initial={"user":self.request.user}, instance=project)
        context["random_status_report"] = models.StatusReport.objects.first()

        context["file_form"] = forms.FileForm
        context["random_file"] = models.File.objects.first()

        context["btn_class_1"] = "create-btn"
        # context["files"] = project.files.all()
        # context["financial_summary_dict"] = financial_summary_data(project)

        # Determine if the user will be able to edit the project.
        # context["can_edit"] = can_modify_project(self.request.user, project.id)
        # context["is_lead"] = self.request.user in [staff.user for staff in project.staff_members.filter(lead=True)]
        return context


class ProjectUpdateView(CanModifyProjectRequiredMixin, CommonUpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'projects2/project_form.html'
    home_url_name = "projects2:index"
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("projects2:project_detail", args=[self.get_object().id])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context

    def get_initial(self):
        return dict(modified_by=self.request.user)


class ProjectDeleteView(CanModifyProjectRequiredMixin, CommonDeleteView):
    model = models.Project
    delete_protection = False
    home_url_name = "projects2:index"
    success_url = reverse_lazy("projects2:index")
    template_name = "projects2/confirm_delete.html"
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("projects2:project_detail", args=[self.get_object().id])}


class ProjectCloneView(ProjectUpdateView):
    template_name = 'projects2/project_form.html'

    def get_h1(self):
        return _("Cloning: ") + str(self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloning"] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:login_required'))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        obj = self.get_object()
        init = super().get_initial()
        init["title"] = f"CLONE OF: {obj.title}"
        init["cloning"] = True
        return init

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.Project.objects.get(pk=new_obj.pk)

        new_obj.project = new_obj
        new_obj.pk = None
        new_obj.save()

        for t in old_obj.tags.all():
            new_obj.tags.add(t)

        # for each year of old project, clone into new project...
        for old_year in old_obj.years.all():
            new_year = deepcopy(old_year)

            new_year.project = new_obj
            new_year.pk = None
            new_year.submitted = None
            new_year.allocated_budget = None
            new_year.status = 1
            new_year.notification_email_sent = None
            new_year.save()

            # Now we need to replicate all the related records:
            # 1) staff
            for old_rel_obj in old_year.staff_set.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # we have to just make sure that the user is a lead on the project. Otherwise they will not be able to edit.
            my_staff, created = models.Staff.objects.get_or_create(
                user=self.request.user,
                project_year=new_year,
                employee_type_id=1,
            )
            my_staff.lead = True
            my_staff.save()

            # 2) O&M
            for old_rel_obj in old_year.omcost_set.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 3) Capital
            for old_rel_obj in old_year.capitalcost_set.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 4) G&C
            for old_rel_obj in old_year.gc_costs.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 5) Collaborators and Partners
            for old_rel_obj in old_year.collaborators.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 6) Collaborative Agreements
            for old_rel_obj in old_year.agreements.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.save()

            # 7) Milestones
            for old_rel_obj in old_year.milestones.all():
                new_rel_obj = deepcopy(old_rel_obj)
                new_rel_obj.pk = None
                new_rel_obj.project_year = new_year
                new_rel_obj.target_date = None  # clear the target date
                new_rel_obj.save()

        return HttpResponseRedirect(reverse_lazy("projects2:project_detail", kwargs={"pk": new_obj.project.id}))


# PROJECT YEAR #
################


class ProjectYearCreateView(CanModifyProjectRequiredMixin, CommonCreateView):
    model = models.ProjectYear
    form_class = forms.ProjectYearForm
    home_url_name = "projects2:index"
    template_name = 'projects2/project_year_form.html'
    container_class = "container bg-light curvy"

    def get_initial(self):
        # this is an important method to keep since it is accessed by the Form class 
        # TODO: TEST ME
        return dict(project=self.get_project())

    def get_project(self):
        return models.Project.objects.get(pk=self.kwargs["project"])

    def get_parent_crumb(self):
        return {"title": self.get_project(), "url": reverse_lazy("projects2:project_detail", args=[self.get_project().id])}

    def form_valid(self, form):
        year = form.save(commit=False)
        year.modified_by = self.request.user
        year.save()

        return HttpResponseRedirect(
            super().get_success_url() + f"?project_year={year.id}"
        )


class ProjectYearUpdateView(CanModifyProjectRequiredMixin, CommonUpdateView):
    model = models.ProjectYear
    form_class = forms.ProjectYearForm
    home_url_name = "projects2:index"
    template_name = 'projects2/project_year_form.html'
    container_class = "container bg-light curvy"

    def get_h1(self):
        return _("Edit ") + str(self.get_object())

    def get_project(self):
        return self.get_object().project

    def get_parent_crumb(self):
        return {"title": self.get_project(), "url": reverse_lazy("projects2:project_detail", args=[self.get_project().id])}

    def form_valid(self, form):
        year = form.save(commit=False)
        year.modified_by = self.request.user
        year.save()
        return super().form_valid(form)

    def get_success_url(self):
        return super().get_success_url() + f"?project_year={self.get_object().id}"


class ProjectYearDeleteView(CanModifyProjectRequiredMixin, CommonDeleteView):
    model = models.ProjectYear
    delete_protection = False
    home_url_name = "projects2:index"
    template_name = "projects2/confirm_delete.html"
    container_class = "container bg-light curvy"

    def get_grandparent_crumb(self):
        return {"title": self.get_project(), "url": reverse("projects2:project_detail", args=[self.get_project().id])}

    def get_project(self):
        return self.get_object().project

    def delete(self, request, *args, **kwargs):
        project = self.get_project()
        self.get_object().delete()
        project.save()
        return HttpResponseRedirect(reverse("projects2:project_detail", args=[project.id]))


class ProjectYearCloneView(ProjectYearUpdateView):
    template_name = 'projects2/project_year_form.html'

    def get_h1(self):
        return _("Cloning: ") + str(self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloning"] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:login_required'))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        init = super().get_initial()
        init["start_date"] = timezone.now()
        init["cloning"] = True
        return init

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.ProjectYear.objects.get(pk=new_obj.pk)

        new_obj.pk = None
        new_obj.submitted = None
        new_obj.allocated_budget = None
        new_obj.status = 1
        new_obj.notification_email_sent = None
        new_obj.save()

        # Now we need to replicate all the related records:
        # 1) staff
        for old_rel_obj in old_obj.staff_set.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # we have to just make sure that the user is a lead on the project. Otherwise they will not be able to edit.
        my_staff, created = models.Staff.objects.get_or_create(
            user=self.request.user,
            project_year=new_obj,
            employee_type_id=1,
        )
        my_staff.lead = True
        my_staff.save()

        # 2) O&M
        for old_rel_obj in old_obj.omcost_set.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 3) Capital
        for old_rel_obj in old_obj.capitalcost_set.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 4) G&C
        for old_rel_obj in old_obj.gc_costs.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 5) Collaborators and Partners
        for old_rel_obj in old_obj.collaborators.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 6) Collaborative Agreements
        for old_rel_obj in old_obj.agreements.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.save()

        # 7) Milestones
        for old_rel_obj in old_obj.milestones.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.project_year = new_obj
            new_rel_obj.target_date = None  # clear the target date
            new_rel_obj.save()

        return HttpResponseRedirect(reverse_lazy("projects2:project_detail", kwargs={"pk": new_obj.project.id}))


# FUNCTIONAL GROUPS #
#####################

class FunctionalGroupListView(AdminRequiredMixin, CommonFilterView):
    template_name = 'projects2/list.html'
    filterset_class = filters.FunctionalGroupFilter
    home_url_name = "projects2:index"
    new_object_url = reverse_lazy("projects2:group_new")
    row_object_url_name = row_ = "projects2:group_edit"
    container_class = "container-fluid bg-light curvy"

    field_list = [
        {"name": 'tname|{}'.format("name"), "class": "", "width": ""},
        {"name": 'theme', "class": "", "width": ""},
        {"name": 'sections', "class": "", "width": "600px"},
    ]

    def get_queryset(self):
        return models.FunctionalGroup.objects.annotate(
            search_term=Concat('name', Value(" "), 'nom', Value(" "), output_field=TextField()))


class FunctionalGroupUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.FunctionalGroup
    form_class = forms.FunctionalGroupForm
    template_name = 'projects2/form.html'
    home_url_name = "projects2:index"
    parent_crumb = {"title": gettext_lazy("Functional Groups"), "url": reverse_lazy("projects2:group_list")}
    container_class = "container bg-light curvy"


class FunctionalGroupCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.FunctionalGroup
    form_class = forms.FunctionalGroupForm
    success_url = reverse_lazy('projects2:group_list')
    template_name = 'projects2/form.html'
    home_url_name = "projects2:index"
    parent_crumb = {"title": gettext_lazy("Functional Groups"), "url": reverse_lazy("projects2:group_list")}
    container_class = "container bg-light curvy"


class FunctionalGroupDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.FunctionalGroup
    success_url = reverse_lazy('projects2:group_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'projects2/confirm_delete.html'
    container_class = "container bg-light curvy"


# SETTINGS #
############
class FundingSourceHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.FundingSource
    success_url = reverse_lazy("projects2:manage_funding_sources")


class FundingSourceFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Funding Source"
    queryset = models.FundingSource.objects.all()
    formset_class = forms.FundingSourceFormset
    success_url = reverse_lazy("projects2:manage_funding_sources")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_funding_source"
    container_class = "container bg-light curvy"


class OMCategoryHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.OMCategory
    success_url = reverse_lazy("projects2:manage_om_cats")


class OMCategoryFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage OMCategory"
    queryset = models.OMCategory.objects.all()
    formset_class = forms.OMCategoryFormset
    success_url = reverse_lazy("projects2:manage_om_cats")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_om_cat"
    container_class = "container bg-light curvy"


class EmployeeTypeHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.EmployeeType
    success_url = reverse_lazy("projects2:manage_employee_types")


class EmployeeTypeFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Employee Type"
    queryset = models.EmployeeType.objects.all()
    formset_class = forms.EmployeeTypeFormset
    success_url = reverse_lazy("projects2:manage_employee_types")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_employee_type"
    container_class = "container bg-light curvy"


class TagHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.Tag
    success_url = reverse_lazy("projects2:manage_tags")


class TagFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Tag"
    queryset = models.Tag.objects.all()
    formset_class = forms.TagFormset
    success_url = reverse_lazy("projects2:manage_tags")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_tag"
    container_class = "container bg-light curvy"


class HelpTextHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.HelpText
    success_url = reverse_lazy("projects2:manage_help_text")


class HelpTextFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Help Text"
    queryset = models.HelpText.objects.all()
    formset_class = forms.HelpTextFormset
    success_url = reverse_lazy("projects2:manage_help_text")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_help_text"
    container_class = "container bg-light curvy"


class LevelHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.Level
    success_url = reverse_lazy("projects2:manage_levels")


class LevelFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Level"
    queryset = models.Level.objects.all()
    formset_class = forms.LevelFormset
    success_url = reverse_lazy("projects2:manage_levels")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_level"
    container_class = "container bg-light curvy"


class ActivityTypeHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.ActivityType
    success_url = reverse_lazy("projects2:manage_activity_types")


class ActivityTypeFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Activity Type"
    queryset = models.ActivityType.objects.all()
    formset_class = forms.ActivityTypeFormset
    success_url = reverse_lazy("projects2:manage_activity_types")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_activity_type"
    container_class = "container bg-light curvy"


class ThemeHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.Theme
    success_url = reverse_lazy("projects2:manage_themes")


class ThemeFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Theme"
    queryset = models.Theme.objects.all()
    formset_class = forms.ThemeFormset
    success_url = reverse_lazy("projects2:manage_themes")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete_theme"
    container_class = "container bg-light curvy"


class UpcomingDateHardDeleteView(AdminRequiredMixin, CommonHardDeleteView):
    model = models.UpcomingDate
    success_url = reverse_lazy("projects2:manage-upcoming-dates")


class UpcomingDateFormsetView(AdminRequiredMixin, CommonFormsetView):
    template_name = 'projects2/formset.html'
    h1 = "Manage Upcoming Dates"
    queryset = models.UpcomingDate.objects.all()
    formset_class = forms.UpcomingDateFormset
    success_url = reverse_lazy("projects2:manage-upcoming-dates")
    home_url_name = "projects2:index"
    delete_url_name = "projects2:delete-upcoming-date"
    container_class = "container bg-light curvy"


# Reference Materials
class ReferenceMaterialListView(AdminRequiredMixin, CommonListView):
    template_name = "projects2/list.html"
    model = models.ReferenceMaterial
    field_list = [
        {"name": "tname|{}".format(gettext_lazy("name")), "class": "", "width": ""},
        {"name": "region", "class": "", "width": ""},
        {"name": "file_display_en|{}".format(gettext_lazy("File attachment (EN)")), "class": "", "width": ""},
        {"name": "file_display_fr|{}".format(gettext_lazy("File attachment (FR)")), "class": "", "width": ""},
        {"name": "date_created", "class": "", "width": ""},
        {"name": "date_modified", "class": "", "width": ""},
    ]
    new_object_url_name = "projects2:ref_mat_new"
    row_object_url_name = "projects2:ref_mat_edit"
    home_url_name = "projects2:index"
    h1 = gettext_lazy("Reference Materials")
    container_class = "container bg-light curvy"


class ReferenceMaterialUpdateView(AdminRequiredMixin, CommonUpdateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "projects2:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("projects2:ref_mat_list")}
    template_name = "projects2/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"

    def get_delete_url(self):
        return reverse("projects2:ref_mat_delete", args=[self.get_object().id])


class ReferenceMaterialCreateView(AdminRequiredMixin, CommonCreateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "projects2:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("projects2:ref_mat_list")}
    template_name = "projects2/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"


class ReferenceMaterialDeleteView(AdminRequiredMixin, CommonDeleteView):
    model = models.ReferenceMaterial
    success_url = reverse_lazy('projects2:ref_mat_list')
    home_url_name = "projects2:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("projects2:ref_mat_list")}
    template_name = "projects2/confirm_delete.html"
    delete_protection = False
    container_class = "container bg-light curvy"



# STATUS REPORT #
#################


class StatusReportDeleteView(CanModifyProjectRequiredMixin, CommonDeleteView):
    template_name = "projects/status_report_confirm_delete.html"
    model = models.StatusReport

    def get_success_url(self, **kwargs):
        return reverse_lazy("shared_models:close_me")


class StatusReportDetailView(LoginRequiredMixin, CommonDetailView):
    model = models.StatusReport
    home_url_name = "projects2:index"
    template_name = "projects2/status_report_detail.html"
    field_list = get_status_report_field_list()


    def dispatch(self, request, *args, **kwargs):
        # when the view loads, let's make sure that all the milestones are on the project.
        my_object = self.get_object()
        my_project_year = my_object.project_year
        for milestone in my_project_year.milestones.all():
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

    def get_project_year(self):
        return self.get_object().project_year

    def get_parent_crumb(self):
        return {"title": str(self.get_project_year().project), "url": reverse_lazy("projects2:project_detail", args=[self.get_project_year().project.id]) + f"?project_year={self.get_project_year().id}"}

    # def get_pdf_filename(self):
    #     my_report = models.StatusReport.objects.get(pk=self.kwargs["pk"])
    #     pdf_filename = "{}.pdf".format(
    #         my_report
    #     )
    #     return pdf_filename

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
