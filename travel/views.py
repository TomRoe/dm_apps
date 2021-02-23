import json
import os
from copy import deepcopy

from azure.storage.blob import BlockBlobService
from decouple import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.db.models import Sum, Q, Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy
from django.views.generic import UpdateView, DeleteView, CreateView, FormView
###
from easy_pdf.views import PDFTemplateView
from msrestazure.azure_active_directory import MSIAuthentication

from dm_apps.context_processor import my_envr
from dm_apps.utils import custom_send_mail, compare_strings
from lib.functions.custom_functions import fiscal_year
from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from shared_models.views import CommonFormsetView, CommonHardDeleteView, CommonUpdateView, CommonFilterView, CommonFormView, \
    CommonPopoutFormView, CommonPopoutUpdateView, CommonListView, CommonDetailView, CommonTemplateView, CommonCreateView, CommonDeleteView
from . import emails
from . import filters
from . import forms
from . import models
from . import reports
from . import utils
from .mixins import TravelAccessRequiredMixin, CanModifyMixin, TravelAdminRequiredMixin, AdminOrApproverRequiredMixin, TravelADMAdminRequiredMixin
from .utils import in_travel_admin_group, in_adm_admin_group, can_modify_request, is_approver, is_trip_approver, is_manager_or_assistant_or_admin


def get_file(request, file):
    if request.GET.get("reference"):
        my_file = models.ReferenceMaterial.objects.get(pk=int(file))
        blob_name = my_file.tfile
        export_file_name = blob_name
    elif request.GET.get("blob_name"):
        blob_name = file.replace("||", "/")
        export_file_name = blob_name.split("/")[-1]
        if request.GET.get("export_file_name"):
            export_file_name = request.GET.get("export_file_name")
    else:
        my_file = models.File.objects.get(pk=int(file))
        blob_name = my_file.file
        export_file_name = blob_name

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        AZURE_STORAGE_ACCOUNT_NAME = settings.AZURE_STORAGE_ACCOUNT_NAME
        AZURE_MSI_CLIENT_ID = config("AZURE_MSI_CLIENT_ID", cast=str, default="")
        account_key = config("AZURE_STORAGE_SECRET_KEY", default=None)
        try:
            token_credential = MSIAuthentication(resource=f'https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net', client_id=AZURE_MSI_CLIENT_ID)
        except Exception as E:
            print(E)
            token_credential = None
        blobService = BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT_NAME, token_credential=token_credential, account_key=account_key)
        blob_file = blobService.get_blob_to_bytes("media", blob_name)
        response = HttpResponse(blob_file.content, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{export_file_name}"'
    else:
        response = HttpResponse(blob_name.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{export_file_name}"'

    return response


def get_conf_details(request):
    """ used exclusively for the request_form but should be phased out with REST Api"""
    conf_dict = {}
    qs = models.Conference.objects.filter(start_date__gte=timezone.now())
    for conf in qs:
        conf_dict[conf.id] = {}
        conf_dict[conf.id]['location'] = conf.location
        conf_dict[conf.id]['start_date'] = conf.start_date.strftime("%Y-%m-%d")
        conf_dict[conf.id]['end_date'] = conf.end_date.strftime("%Y-%m-%d")
        if conf.date_eligible_for_adm_review and timezone.now() > conf.date_eligible_for_adm_review:
            conf_dict[conf.id]['is_late_request'] = True
        else:
            conf_dict[conf.id]['is_late_request'] = False
    return JsonResponse(conf_dict)


class IndexTemplateView(TravelAccessRequiredMixin, CommonTemplateView):
    template_name = 'travel/index/main.html'
    active_page_name_crumb = gettext_lazy("Home")
    h1 = " "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["processes"] = [
            models.ProcessStep.objects.filter(stage=1),
            models.ProcessStep.objects.filter(stage=2)
        ]
        context["information_sections"] = models.ProcessStep.objects.filter(stage=0, is_visible=True)
        context["faqs"] = models.FAQ.objects.all()
        context["refs"] = models.ReferenceMaterial.objects.all()
        # context["region_tabs"] = [region.tname for region in shared_models.Region.objects.all()]

        context["is_admin"] = in_travel_admin_group(self.request.user)
        context["is_adm_admin"] = in_adm_admin_group(self.request.user)
        context["can_see_all_requests"] = is_manager_or_assistant_or_admin(self.request.user)

        return context


conf_field_list = [
    'tname|{}'.format(gettext_lazy("Name")),
    'location',
    'trip_subcategory',
    'lead',
    'has_event_template',
    'number',
    'start_date',
    'end_date',
    'meeting_url',
    'abstract_deadline',
    'registration_deadline',
    'is_adm_approval_required',
    'notes',
    'status_string|{}'.format("status"),
    'date_eligible_for_adm_review',
    'adm_review_deadline',
    'total_cost|{}'.format(gettext_lazy("Total DFO cost (excluding BTA)")),
    'non_res_total_cost|{}'.format(gettext_lazy("Total DFO cost from non-RES travellers (excluding BTA)")),
]


def get_help_text_dict():
    my_dict = {}
    for obj in models.HelpText.objects.all():
        my_dict[obj.field_name] = str(obj)

    return my_dict


# Requests #
################
class TripRequestListView(TravelAccessRequiredMixin, CommonTemplateView):
    template_name = 'travel/request_list/main.html'
    subtitle = gettext_lazy("Trip Requests")
    home_url_name = "travel:index"
    container_class = "container-fluid"
    row_object_url_name = "travel:request_detail"
    h1 = _("Trip Requests")

    field_list = [
        'fiscal_year',
        'created_by',
        'trip.tname|{}'.format(gettext_lazy("trip")),
        'trip.location|{}'.format(gettext_lazy("Destination")),
        'travellers|{}'.format(gettext_lazy("travellers")),
        'status',
        'section',
        'processing_time|{}'.format(gettext_lazy("Processing time")),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_object"] = models.TripRequest1.objects.first()
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in models.TripRequest1.status_choices]

        return context

    def get_new_object_url(self):
        return reverse("travel:request_new")


class TripRequestDetailView(TravelAccessRequiredMixin, CommonDetailView):
    model = models.TripRequest1
    template_name = 'travel/request_detail.html'
    home_url_name = "travel:index"

    def get_context_data(self, **kwargs):
        my_object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["trip_request"] = self.get_object()
        # context['random_request_reviewer'] = models.Reviewer.objects.first()
        return context


class TripRequestUpdateView(CanModifyMixin, CommonUpdateView):
    model = models.TripRequest1
    home_url_name = "travel:index"
    h1 = gettext_lazy("Edit Trip Request")
    template_name = 'travel/request_form.html'
    form_class = forms.TripRequestForm

    def get_initial(self):
        return {"reset_reviewers": False}

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def form_valid(self, form):
        my_object = form.save(commit=False)
        # if by mistake there is no owner, assign one now
        if not my_object.created_by:
            my_object.created_by = self.request.user
        my_object.save()

        utils.manage_trip_warning(my_object.trip, self.request)

        # decide whether the reviewers should be reset
        if form.cleaned_data.get("reset_reviewers"):
            reset_request_reviewers(self.request, pk=my_object.pk)

        if form.cleaned_data.get("stay_on_page"):
            return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs=self.kwargs))
        else:
            return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs=self.kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_dict = {}
        for user in User.objects.all():
            user_dict[user.id] = {}
            user_dict[user.id]['first_name'] = user.first_name
            user_dict[user.id]['last_name'] = user.last_name
            user_dict[user.id]['email'] = user.email

        user_json = json.dumps(user_dict)
        # send JSON file to template so that it can be used by js script
        context['user_json'] = user_json
        context['org_form'] = forms.OrganizationForm1
        context['help_text_dict'] = get_help_text_dict()
        return context


class TripRequestCreateView(TravelAccessRequiredMixin, CommonCreateView):
    model = models.TripRequest1
    home_url_name = "travel:index"
    h1 = gettext_lazy("New Trip Request")
    form_class = forms.TripRequestForm
    template_name = 'travel/request_form.html'

    def get_initial(self):
        if self.request.GET.get("trip"):
            return dict(trip=self.request.GET.get("trip"))

    def form_valid(self, form):
        my_object = form.save(commit=False)
        my_object.created_by = self.request.user
        my_object.save()

        # add user as traveller if asked to
        if form.cleaned_data.get("is_traveller", None):
            # just make sure they are not already on another trip!!
            if not models.Traveller.objects.filter(request__trip=my_object.trip, user=self.request.user).exists():
                t = models.Traveller.objects.create(
                    request=my_object,
                    user=self.request.user,
                    start_date=my_object.trip.start_date,
                    end_date=my_object.trip.end_date,
                )
                utils.populate_traveller_costs(self.request, t)

        # add reviewers
        utils.get_request_reviewers(my_object)
        return HttpResponseRedirect(reverse_lazy("travel:request_detail", args=[my_object.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context


class TripRequestDeleteView(CanModifyMixin, CommonDeleteView):
    model = models.TripRequest1
    delete_protection = False
    home_url_name = "travel:index"
    template_name = 'travel/confirm_delete.html'

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def get_success_url(self):
        return reverse("travel:request_list")

    def delete(self, request, *args, **kwargs):
        my_object = self.get_object()
        my_object.delete()
        utils.manage_trip_warning(my_object.trip, self.request)
        return HttpResponseRedirect(self.get_success_url())


class TripRequestCloneUpdateView(TripRequestUpdateView):
    h1 = gettext_lazy("Clone a Trip Request")
    h2 = gettext_lazy("Please update the request details")

    def test_func(self):
        if self.request.user.id:
            return True

    def get_initial(self):
        my_object = models.TripRequest1.objects.get(pk=self.kwargs["pk"])
        init = super().get_initial()
        init["year"] = fiscal_year(sap_style=True, next=True)
        init["user"] = self.request.user
        # init["created_by"] = self.request.user
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.TripRequest1.objects.get(pk=new_obj.pk)
        new_obj.pk = None
        new_obj.status = 8
        new_obj.submitted = None
        new_obj.original_submission_date = None
        new_obj.created_by = self.request.user
        new_obj.admin_notes = None

        try:
            new_obj.save()
        except IntegrityError:
            messages.error(self.request, _("sorry, cannot clone this trip because there is another trip request with the same user in the system"))
        return HttpResponseRedirect(reverse_lazy("travel:request_detail", kwargs={"pk": new_obj.id}))


class ChildTripRequestCloneUpdateView(TripRequestUpdateView):
    def test_func(self):
        if self.request.user.id:
            return True

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.TripRequest1.objects.get(pk=new_obj.pk)
        new_obj.pk = None
        new_obj.submitted = None
        new_obj.save()

        # costs
        for old_rel_obj in old_obj.trip_request_costs.all():
            new_rel_obj = deepcopy(old_rel_obj)
            new_rel_obj.pk = None
            new_rel_obj.trip_request = new_obj
            new_rel_obj.save()

        return HttpResponseRedirect(reverse_lazy("travel:request_edit", kwargs={"pk": new_obj.id}))

    def get_initial(self):
        init = super().get_initial()
        init["user"] = None
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context


class TripRequestSubmitUpdateView(CanModifyMixin, CommonUpdateView):
    model = models.TripRequest1
    form_class = forms.TripRequestApprovalForm
    template_name = 'travel/request_submit.html'
    submit_text = gettext_lazy("Proceed")
    home_url_name = "travel:index"

    def get_submit_text(self):
        my_object = self.get_object()
        if my_object.submitted or not my_object.is_late_request:
            return _("Proceed")
        else:
            return _("Proceed with late submission")

    def get_active_page_name_crumb(self):
        my_object = self.get_object()
        if my_object.submitted:
            return _("Un-submit request")
        else:
            return _("Re-submit request") if my_object.status == 16 else _("Submit request")

    def get_h1(self):
        my_object = self.get_object()

        if my_object.submitted:
            return _("Do you wish to un-submit the following request?")
        else:
            if not my_object.is_late_request:
                return _("Do you wish to re-submit the following request?") if my_object.status == 16 else _(
                    "Do you wish to submit the following request?")
            else:
                return _("Do you wish to re-submit the following late request?") if my_object.status == 16 else _(
                    "Do you wish to submit the following late request?")

    def get_h2(self):
        my_object = self.get_object()
        if my_object.submitted:
            return '<span class="red-font">WARNING: Un-submitting this request will reset the' \
                   ' status of any existing recommendations and/or approvals.</span>'

    def test_func(self):
        # This view is a little different. A trip owner should always be allowed to unsubmit
        return can_modify_request(self.request.user, self.kwargs.get("pk"), True)

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        context["trip_request"] = self.get_object()

        return context

    def form_valid(self, form):
        my_object = form.save(commit=False)  # There is nothing really to save here. I am just using the machinery of UpdateView (djf)
        # figure out the current state of the request
        my_object.updated_by = self.request.user
        is_submitted = True if my_object.submitted else False

        # if submitted, then unsumbit but only if admin or owner
        if is_submitted:
            #  UNSUBMIT REQUEST
            if in_travel_admin_group(self.request.user) or my_object.user == self.request.user:
                my_object.submitted = None
                my_object.status = 8
                my_object.save()
                # reset all the reviewer statuses
                utils.end_request_review_process(my_object)
            else:
                messages.error(self.request, "sorry, only admins or owners can un-submit requests")
        else:
            if my_object.is_late_request:
                # if the user is submitting a late request, we have to tag NCR Travel Coordinator as the first reviewer
                ## get the NCR travel coordinator; reviewer_role = 3
                ncr_coord = models.DefaultReviewer.objects.filter(reviewer_roles=3).distinct().order_by("order").first()
                ## in the case that there is not an ncr travel coordinator, we cannot do this!
                if ncr_coord:
                    reviewer, created = models.Reviewer.objects.get_or_create(
                        request=my_object,
                        user=ncr_coord.user,
                        role=3,
                    )
                    reviewer.order = -1000000
                    reviewer.save()

            #  SUBMIT REQUEST
            my_object.submitted = timezone.now()
            # if there is not an original submission date, add one
            if not my_object.original_submission_date:
                my_object.original_submission_date = timezone.now()
            # if the request is being resubmitted, this is a special case...
            if my_object.status == 16:
                my_object.status = 8  # it doesn't really matter what we set the status to. The approval_seeker func will handle this
                my_object.save()
            else:
                # set all the reviewer statuses to 'queued'
                utils.start_request_review_process(my_object)
                # go and get approvals!!

            # clean up any unused cost categories
            for traveller in my_object.travellers.all():
                utils.clear_empty_traveller_costs(traveller)

        # No matter what business was done, we will call this function to sort through reviewer and request statuses
        utils.approval_seeker(my_object, False, self.request)
        my_object.save()

        return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs))


class TripRequestCancelUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    model = models.TripRequest1
    form_class = forms.TripRequestAdminNotesForm
    template_name = 'travel/form.html'
    h1 = gettext_lazy("Do you wish to cancel the following trip request?")
    active_page_name_crumb = gettext_lazy("Cancel request")
    submit_text = gettext_lazy("Proceed")

    def get_h2(self):
        return "<span class='red-font blink-me'>" + \
               _("Please note that this action cannot be undone!!") + \
               "</span>"

    def get_h3(self):
        return str(self.get_object())

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse_lazy("travel:request_detail", kwargs=self.kwargs)}

    def get_context_data(self, **kwargs):
        my_object = self.get_object()
        # figure out the current state of the request
        # is_cancelled = True if my_object.status == 22 else False
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        my_trip_request = form.save(commit=False)
        my_trip_request.updated_by = self.request.user
        my_trip_request.save()

        # figure out the current state of the request
        is_cancelled = True if my_trip_request.status == 22 else False

        if is_cancelled:
            messages.warning(self.request, _("Sorry, it is currently not possible to cancel your cancellation "))
            return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs))

            # UN-CANCEL THE REQUEST
            # my_trip_request.status = 11
        else:
            #  CANCEL THE REQUEST
            my_trip_request.status = 22
            my_trip_request.save()

            # cancel any outstanding reviews:
            # but only those with the following statuses: PENDING = 1; QUEUED = 20;
            tr_reviewer_statuses_of_interest = [1, 20, ]
            for r in my_trip_request.reviewers.filter(status__in=tr_reviewer_statuses_of_interest):
                r.status = 5
                r.save()

            # send an email to the trip_request owner
            email = emails.StatusUpdateEmail(my_trip_request, self.request)
            # # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
            return HttpResponseRedirect(reverse("travel:request_detail", kwargs=self.kwargs))


# TRIP REQUEST REVIEWER #
#########################

class TripRequestReviewerListView(TravelAccessRequiredMixin, CommonTemplateView):
    model = models.Reviewer
    template_name = 'travel/request_reviewer_list.html'
    home_url_name = "travel:index"
    h1 = " "
    active_page_name_crumb = gettext_lazy("Request reviews")

    def get_queryset(self):
        return utils.get_related_request_reviewers(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TripRequestReviewerUpdateView(AdminOrApproverRequiredMixin, CommonUpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerApprovalForm
    template_name = 'travel/request_reviewer_update.html'
    home_url_name = "travel:index"

    def get_query_string(self):
        if nz(self.request.META['QUERY_STRING'], None):
            return "?" + self.request.META['QUERY_STRING']
        return ""

    def get_h1(self):
        if self.request.GET.get("rdg"):
            return _("Do you wish to approve on behalf of {user} ({role})".format(
                user=self.get_object().user,
                role=self.get_object().get_role_display(),
            ))
        return _("Do you wish to approve the following request?")

    def get_parent_crumb(self):
        return {"title": _("Requests Awaiting Review"), "url": reverse("travel:request_reviewer_list") + self.get_query_string()}

    def test_func(self):
        my_trip_request = self.get_object().request
        my_user = self.request.user
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip_request"] = self.get_object().request
        context['help_text_dict'] = get_help_text_dict()
        return context

    def form_valid(self, form):
        # don't save the reviewer yet because there are still changes to make
        my_reviewer = form.save(commit=True)

        approved = form.cleaned_data.get("approved")
        stay_on_page = form.cleaned_data.get("stay_on_page")
        changes_requested = form.cleaned_data.get("changes_requested")
        # first scenario: changes were requested for the request
        # in this case, the reviewer status does not change but the request status will
        if not stay_on_page:
            if changes_requested:
                my_reviewer.request.status = 16
                my_reviewer.request.submitted = None
                my_reviewer.request.save()
                # send an email to the request owner
                email = emails.ChangesRequestedEmail(my_reviewer.request, self.request)
                # send the email object
                custom_send_mail(
                    subject=email.subject,
                    html_message=email.message,
                    from_email=email.from_email,
                    recipient_list=email.to_list
                )
                messages.success(self.request, _("Success! An email has been sent to the trip request owner."))

            # if it was approved, then we change the reviewer status to 'approved'
            elif approved:
                my_reviewer.status = 2
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()
            # if it was not approved, then we change the reviewer status to 'denied'
            else:
                my_reviewer.status = 3
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()

            # update any statuses if necessary
            utils.approval_seeker(my_reviewer.request, False, self.request)

        if stay_on_page:
            return HttpResponseRedirect(reverse("travel:request_reviewer_update", args=[my_reviewer.id]) + self.get_query_string() + "#id_comments")
        else:
            return HttpResponseRedirect(reverse("travel:request_reviewer_list") + self.get_query_string())


# class TripRequestAdminApprovalListView(TravelAdminRequiredMixin, CommonListView):
#     model = models.TripRequest1
#     template_name = 'travel/trip_request_review_list.html'
#     home_url_name = "travel:index"
#     field_list = [
#         {"name": 'is_group_request', "class": "", "width": ""},
#         {"name": 'first_name', "class": "", "width": ""},
#         {"name": 'last_name', "class": "", "width": ""},
#         {"name": 'trip', "class": "", "width": ""},
#         {"name": 'destination', "class": "", "width": ""},
#         {"name": 'start_date', "class": "", "width": ""},
#         {"name": 'end_date', "class": "", "width": ""},
#         {"name": 'total_request_cost|{}'.format(_("Total cost (DFO)")), "class": "", "width": ""},
#     ]
#
#     def get_h1(self):
#         return _("Admin Request Approval List") + ' ({})'.format(_(self.kwargs.get("type")).upper())
#
#     def get_queryset(self):
#         # return a list only of those awaiting ADM or RDG approval
#         qs = models.TripRequest1.objects.filter(parent_request__isnull=True).order_by("-submitted")
#         if self.kwargs.get("type") == "adm":
#             qs = qs.filter(status=14)
#         elif self.kwargs.get("type") == "rdg":
#             qs = qs.filter(status=15)
#         if self.kwargs.get("region"):
#             qs = qs.filter(section__division__branch__region_id=self.kwargs.get("region"))
#
#         return qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context["random_object"] = models.TripRequest1.objects.first()
#         context["admin"] = True
#         context["type_bilingual"] = _(self.kwargs.get("type")).upper()
#         return context


class TripRequestReviewerADMUpdateView(AdminOrApproverRequiredMixin, CommonPopoutUpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerApprovalForm

    # template_name = 'travel/adm_reviewer_approval_form.html'

    def get_h1(self):
        if self.kwargs.get("approve") == 1:
            return _("Do you wish to approve the following request for {}".format(
                self.get_object().trip_request.requester_name
            ))
        else:
            return _("Do you wish to deny the following request for {}".format(
                self.get_object().trip_request.requester_name
            ))

    def get_h2(self):
        return "<span class='red-font'>{}</span>".format(_("These comments will be visible to the traveller"))

    def get_submit_text(self):
        return _("Approve") if self.kwargs.get("approve") == 1 else _("Deny")

    def get_submit_btn_class(self):
        return "btn-success" if self.kwargs.get("approve") == 1 else "btn-danger"

    def test_func(self):
        my_trip_request = self.get_object().trip_request
        my_user = self.request.user
        # print(in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request))
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        return context

    def form_valid(self, form):
        # don't save the reviewer yet because there are still changes to make
        my_reviewer = form.save(commit=True)
        tr = my_reviewer.request
        parent_request = tr.parent_request

        is_approved = True if self.kwargs.get("approve") == 1 else False

        # if it was approved, then we change the reviewer status to 'approved'
        if is_approved:
            my_reviewer.status = 2
        # if it was denied, then we change the reviewer status to 'denied'
        else:
            my_reviewer.status = 3

        my_reviewer.status_date = timezone.now()
        my_reviewer.save()
        # big fork in process here between individual and child requests...
        # 1) individual request:
        ################
        if not parent_request:
            # update any statuses if necessary; this is business as usual
            utils.approval_seeker(my_reviewer.request, False, self.request)
        else:
            # if this is a child request,
            if my_reviewer.status == 3:
                tr.status = 10
            else:
                tr.status = 11
            tr.save()

            # now we must update the trip reviewer comments so that they are in sync with the child review comments
            # best to make from scratch to avoid complexities with duplicating information
            parent_reviewer = parent_request.adm  # let's hope there is only one
            # let's get all the approved or denied children requests and append the comments to the parent_reviewer
            comments = ""
            for child_request in parent_request.children_requests.filter(status__in=[10, 11]):
                comments += f'{child_request.requester_name} &rarr; {child_request.adm.comments}<br>'
            parent_reviewer.comments = comments
            parent_reviewer.save()

            # if we are at the point where all the children request have been approved or denied,
            # we are ready to make headway on the parent request
            if parent_request.children_requests.filter(status__in=[10, 11]).count() == parent_request.children_requests.all().count():
                # the parent request is approved if there is at least one approved traveller
                if parent_request.children_requests.filter(status=11).count() > 0:
                    parent_reviewer.status = 2
                else:
                    parent_reviewer.status = 3
                parent_reviewer.status_date = timezone.now()
                parent_reviewer.save()

                utils.approval_seeker(parent_request, False, self.request)

            #
            #             # We have to append any comments to the corresponding review of the parent request
            #
            # # TODO: maybe the button should say something like "remove from group request"
            #
            #             parent_request = tr.parent_request
            #             if parent_request.comments:
            #                 pass

            # # send an email to the request owner
            # email = emails.ChangesRequestedEmail(my_reviewer.request)
            # # send the email object
            # custom_send_mail(
            #     subject=email.subject,
            #     html_message=email.message,
            #     from_email=email.from_email,
            #     recipient_list=email.to_list
            # )
            pass

        return HttpResponseRedirect(self.get_success_url())


class SkipReviewerUpdateView(TravelAdminRequiredMixin, CommonPopoutUpdateView):
    model = models.Reviewer
    form_class = forms.ReviewerSkipForm
    template_name = 'shared_models/generic_popout_form.html'

    def get_h1(self):
        return _("Are you certain you wish to skip the following user?")

    def get_h2(self):
        return str(self.get_object())

    def test_func(self):
        my_trip_request = self.get_object().trip_request
        my_user = self.request.user
        # print(in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request))
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def form_valid(self, form):
        # if the form is submitted, that means the admin user has decided to go ahead with the manual skip
        my_reviewer = form.save(commit=False)
        my_reviewer.status = 21
        my_reviewer.status_date = timezone.now()
        my_reviewer.comments = "This reviewer was manually overridden by {} with the following rationale: \n\n {}".format(self.request.user,
                                                                                                                          my_reviewer.comments)
        # now we save the reviewer for real
        my_reviewer.save()
        # update any statuses if necessary
        utils.approval_seeker(my_reviewer.request, False, self.request)

        return HttpResponseRedirect(reverse("shared_models:close_me"))


@login_required(login_url='/accounts/login/')
# @user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def reset_request_reviewers(request, pk):
    """this function will reset the reviewers on either a trip request"""
    my_obj = models.TripRequest1.objects.get(pk=pk)
    if can_modify_request(request.user, pk):
        # This function should only ever be run if the TR is a draft
        if my_obj.status == 8:
            # first remove any existing reviewers
            my_obj.reviewers.all().delete()
            # next, re-add the defaults...
            utils.get_request_reviewers(my_obj)
        else:
            messages.error(request, _("This function can only be used when the trip request is still a draft"))
    else:
        messages.error(request, _("You do not have the permissions to reset the reviewer list"))
    return HttpResponseRedirect(reverse("travel:request_detail", args=(pk,)))


@login_required(login_url='/accounts/login/')
# @user_passes_test(in_travel_admin_group, login_url='/accounts/denied/')
def reset_trip_reviewers(request, trip=None):
    """this function will reset the reviewers on a trip"""
    # first, this should only ever be an ADM admin group
    if not in_adm_admin_group(request.user):
        return HttpResponseForbidden()
    else:
        my_obj = models.Conference.objects.get(pk=trip)
        # This function should only ever be run if the trip is unreviewed (30 = unverified, unreviewer; 41 = verified, reviewed)
        if my_obj.status in [30, 41]:
            # first remove any existing reviewers
            my_obj.reviewers.all().delete()
            # next, re-add the defaults...
            utils.get_trip_reviewers(my_obj)
        else:
            messages.error(request, _("This function can only be used with an unreviewed trip."))
        return HttpResponseRedirect(reverse("travel:trip_detail", args=(trip, type)))


# REVIEWER #
############

class TripRequestReviewerHardDeleteView(CanModifyMixin, CommonHardDeleteView):
    model = models.Reviewer

    def test_func(self):
        my_obj = models.Reviewer.objects.get(pk=self.kwargs.get("pk"))
        if can_modify_request(self.request.user, my_obj.trip_request.id):
            if my_obj.status not in [4, 20]:
                messages.error(self.request, _(f"Sorry, you cannot delete a reviewer who's status is set to {my_obj.get_status_display()}"))
            else:
                return True


class TripReviewerHardDeleteView(TravelADMAdminRequiredMixin, CommonHardDeleteView):
    model = models.TripReviewer

    def test_func(self):
        my_obj = models.TripReviewer.objects.get(pk=self.kwargs.get("pk"))
        if in_travel_admin_group(self.request.user):
            if my_obj.status not in [23, 24]:
                messages.error(self.request, _(f"Sorry, you cannot delete a reviewer who's status is set to {my_obj.get_status_display()}"))
            else:
                return True


@login_required(login_url='/accounts/login/')
# @user_passes_test(is_superuser, login_url='/accounts/denied/')
def manage_reviewers(request, type, triprequest=None, trip=None):
    if triprequest:
        my_trip_request = models.TripRequest1.objects.get(pk=triprequest)
        if can_modify_request(request.user, my_trip_request.id):
            # if not my_trip_request.status in [8, 16]:
            #     messages.error(request, _("Sorry, you will have to unsubmit the trip in order to make this change"))
            #     return HttpResponseRedirect(reverse("travel:request_detail", kwargs={"pk": my_trip_request.id}))
            # else:
            qs = models.Reviewer.objects.filter(trip_request=my_trip_request)
            if request.method == 'POST':
                formset = forms.ReviewerFormset(request.POST)
                if formset.is_valid():
                    formset.save()

                    my_trip_request.save()
                    # do something with the formset.cleaned_data
                    messages.success(request, _("The reviewer list has been successfully updated"))
                    return HttpResponseRedirect(reverse("travel:manage_tr_reviewers", args=(triprequest, type)))
            else:
                formset = forms.ReviewerFormset(
                    queryset=qs,
                    initial=[{"trip_request": my_trip_request}],
                )

            context = dict()
            context['triprequest'] = my_trip_request
            context['formset'] = formset
            context['type'] = type
            context["my_object"] = models.Reviewer.objects.first()
            context["field_list"] = [
                'order',
                'user',
                'role',
            ]
            return render(request, 'travel/reviewer_formset.html', context)
        else:
            messages.error(request, _("You do not have the permissions to modify the reviewer list"))
            return HttpResponseRedirect(reverse("travel:request_detail", args=(triprequest)))
    elif trip:
        my_trip = models.Conference.objects.get(pk=trip)
        if not in_adm_admin_group(request.user):
            return HttpResponseForbidden()
        elif my_trip.status not in [30, 41]:
            messages.error(request, _("Sorry, you cannot modify the reviewers on a trip that is under review."))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            qs = models.TripReviewer.objects.filter(trip=trip)
            if request.method == 'POST':
                formset = forms.TripReviewerFormset(request.POST)
                if formset.is_valid():
                    formset.save()

                    my_trip.save()
                    # do something with the formset.cleaned_data
                    messages.success(request, _("The reviewer list has been successfully updated"))
                    return HttpResponseRedirect(reverse("travel:manage_trip_reviewers", args=(trip, type)))
            else:
                formset = forms.TripReviewerFormset(
                    queryset=qs,
                    initial=[{"trip": my_trip}],
                )

            context = dict()
            context['trip'] = my_trip
            context['type'] = type
            context['formset'] = formset
            context["my_object"] = models.TripReviewer.objects.first()
            context["field_list"] = [
                'order',
                'user',
                'role',
            ]
            return render(request, 'travel/reviewer_formset.html', context)


# TRIP #
########

class TripListView(TravelAccessRequiredMixin, CommonTemplateView):
    template_name = 'travel/trip_list/main.html'
    subtitle = gettext_lazy("Trips")
    home_url_name = "travel:index"
    container_class = "container-fluid"
    h1 = _("Trips")

    field_list = [
        'fiscal_year',
        'status',
        'trip_subcategory',
        'tname|{}'.format(gettext_lazy("title")),
        'location|{}'.format(_("location")),
        'lead|{}'.format(_("region")),
        'abstract_deadline|{}'.format(_("abstract deadline")),
        'registration_deadline',
        'dates|{}'.format(_("trip dates")),
        # 'is_adm_approval_required|{}'.format(_("ADM approval required?")),
        'date_eligible_for_adm_review',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_object"] = models.Conference.objects.first()
        context["status_choices"] = [dict(label=item[1], value=item[0]) for item in models.Conference.status_choices]
        context["subcategory_choices"] = [dict(label=item.tname, value=item.id) for item in models.TripSubcategory.objects.all()]
        return context

    def get_new_object_url(self):
        return reverse("travel:trip_new")


class TripDetailView(TravelAccessRequiredMixin, CommonDetailView):
    model = models.Conference
    template_name = 'travel/trip_detail.html'
    home_url_name = "travel:index"

    def get_query_string(self):
        if nz(self.request.META['QUERY_STRING'], None):
            return "?" + self.request.META['QUERY_STRING']
        return ""

    def get_parent_crumb(self):
            return {"title": _("Trips"), "url": reverse_lazy("travel:trip_list") + self.get_query_string()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TripUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    model = models.Conference
    form_class = forms.TripForm
    home_url_name = "travel:index"

    def get_parent_crumb(self):
        return {"title": str(self.get_object()), "url": reverse("travel:trip_detail", kwargs=self.kwargs)}

    def get_template_names(self):
        return 'travel/trip_form_popout.html' if self.request.GET.get("pop") else 'travel/trip_form.html'

    def form_valid(self, form):
        my_object = form.save(commit=False)
        my_object.updated_by = self.request.user
        my_object.save()
        # This is a bit tricky here. Right now will work with the assumption that we do not ever want to reset the reviewers unless
        # the trip was ADM approval required, and now is not, OR if it wasn't and now it is.
        if my_object.is_adm_approval_required and my_object.reviewers.count() == 0 or not my_object.is_adm_approval_required:
            # Add any trip reviewers to the trip, if adm approval is required.
            # This function will also delete any reviewers if adm approval is not required
            utils.get_trip_reviewers(my_object)
        if self.request.GET.get("pop"):
            return HttpResponseRedirect(reverse("shared_models:close_me"))
        else:
            return HttpResponseRedirect(reverse('travel:trip_detail', kwargs=self.kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context


class TripCloneView(TripUpdateView):
    h1 = gettext_lazy("Clone a Trip")
    h2 = gettext_lazy("Please update the trip details")

    def test_func(self):
        if self.request.user.id:
            return True

    def get_initial(self):
        my_object = models.Conference.objects.get(pk=self.kwargs["pk"])
        init = super().get_initial()
        init["name"] = "CLONE OF: " + my_object.name
        # init["created_by"] = self.request.user
        return init

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cloned"] = True
        return context

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        old_obj = models.Conference.objects.get(pk=new_obj.pk)
        new_obj.pk = None
        new_obj.verified_by = self.request.user
        new_obj.created_by = self.request.user
        new_obj.save()
        return HttpResponseRedirect(reverse_lazy("travel:trip_detail", args=[ new_obj.id]))


class TripCreateView(TravelAccessRequiredMixin, CommonCreateView):
    model = models.Conference
    form_class = forms.TripForm
    home_url_name = "travel:index"

    def get_template_names(self):
        return 'travel/trip_form_popout.html' if self.request.GET.get("pop") else 'travel/trip_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_dict'] = get_help_text_dict()
        return context

    def form_valid(self, form):
        my_object = form.save(commit=False)
        my_object.created_by = self.request.user
        my_object.save()
        # Add any trip reviewers to the trip, if adm approval is required
        utils.get_trip_reviewers(my_object)
        if self.request.GET.get("pop"):
            # create a new email object
            email = emails.NewTripEmail(my_object, self.request)
            # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
            messages.success(self.request, _("The trip has been added to the database!"))
            return HttpResponseRedirect(reverse("shared_models:close_me_no_refresh"))
        else:
            return HttpResponseRedirect(reverse("travel:trip_detail", args=[my_object.id]))


class TripDeleteView(TravelAdminRequiredMixin, CommonDeleteView):
    template_name = 'travel/confirm_delete.html'
    model = models.Conference
    success_message = 'The trip was deleted successfully!'
    delete_protection = False

    def get_success_url(self):
        try:
            if self.kwargs.get("type") == "back_to_verify":
                adm = 1 if self.get_object().is_adm_approval_required else 0
                region = self.get_object().lead.id if adm == 0 else 0
                success_url = reverse_lazy('travel:admin_trip_verification_list', kwargs={"adm": adm, "region": region})
            else:
                my_kwargs = self.kwargs
                del my_kwargs["pk"]
                success_url = reverse_lazy('travel:trip_list', kwargs=my_kwargs)
            return success_url
        except:
            return reverse("travel:index")


class TripReviewProcessUpdateView(TravelADMAdminRequiredMixin, CommonUpdateView):
    model = models.Conference
    form_class = forms.TripTimestampUpdateForm
    template_name = 'travel/form.html'
    submit_text = gettext_lazy("Proceed")

    def get_query_string(self):
        if nz(self.request.META['QUERY_STRING'], None):
            return "?" + self.request.META['QUERY_STRING']
        return ""

    def test_func(self):
        # make sure that this page can only be accessed for active trips (exclude those already reviewed and those canceled)
        return in_adm_admin_group(self.request.user) and not self.get_object().status in [43]

    def get_h1(self):
        if self.get_object().status in [30, 41]:
            return _("Do you wish to start a review on this trip?")
        elif self.get_object().status in [32]:
            return _("Do you wish to re-examine this trip?")
        else:
            return _("Do you wish to end the review of this trip?")

    def get_h2(self):
        if self.get_object().status in [30, 41]:
            return self.get_object()
        elif self.get_object().status in [32]:
            return '<span class="blue-font">Re-opening the review on this trip reset the reviewer statuses but ' \
                   'will keep any existing reviewer comments. <br><br> This process will NOT undo any trip request approvals that ' \
                   'have already been issued in the original review process.</span>'
        else:
            return '<span class="red-font">WARNING: <br><br> stopping the review on this trip will reset the' \
                   ' status of any existing recommendations and/or approvals.</span>'

    def get_subtitle(self):
        return _("Start a Review") if self.get_object().status in [30, 41] else _("End a Review")

    # def get_parent_crumb(self):
    #     return {"title":str(self.get_object()), "url": reverse("travel:trip_detail", kwargs=self.kwargs)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        context["conf_field_list"] = conf_field_list
        context['help_text_dict'] = get_help_text_dict()
        return context

    def form_valid(self, form):
        my_trip = form.save()
        # figure out the current state of the request
        if my_trip.status in [30, 41]:
            is_under_review = False
        else:
            is_under_review = True

        if is_under_review:
            if my_trip.status == 32:
                utils.end_trip_review_process(my_trip, reset=True)
            else:
                utils.end_trip_review_process(my_trip, reset=False)
        else:
            utils.start_trip_review_process(my_trip)
            # go and get approvals!!

        # No matter what business what done, we will call this function to sort through reviewer and request statuses
        utils.trip_approval_seeker(my_trip, self.request)
        my_trip.save()

        # decide where to go. If the request user is the same as the active reviewer for the trip, go right to the review page.
        # otherwise go to the index
        if my_trip.current_reviewer and self.request.user == my_trip.current_reviewer.user:
            return HttpResponseRedirect(reverse("travel:trip_reviewer_update", args=[my_trip.current_reviewer.id]))
        else:
            return HttpResponseRedirect(reverse("travel:trip_detail", kwargs=self.kwargs) + self.get_query_string())


class TripVerifyUpdateView(TravelAdminRequiredMixin, CommonFormView):
    template_name = 'travel/trip_verification_form.html'
    model = models.Conference
    form_class = forms.TripRequestApprovalForm
    home_url_name = "travel:index"
    h1 = gettext_lazy("Verify Trip")

    def test_func(self):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        if my_trip.is_adm_approval_required:
            return in_adm_admin_group(self.request.user)
        else:
            return in_travel_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        context["object"] = my_trip
        context["conf_field_list"] = conf_field_list
        context["trip_subcategories"] = models.TripSubcategory.objects.all()

        base_qs = models.Conference.objects.filter(~Q(id=my_trip.id)).filter(fiscal_year=my_trip.fiscal_year)

        context["same_day_trips"] = base_qs.filter(Q(start_date=my_trip.start_date) | Q(end_date=my_trip.end_date))
        context["same_location_trips"] = base_qs.filter(
            id__in=[trip.id for trip in base_qs if trip.location and my_trip.location and
                    compare_strings(trip.location, my_trip.location) < 3]
        )
        similar_fr_name_trips = [trip.id for trip in base_qs if
                                 trip.nom and compare_strings(trip.nom, trip.name) < 15] if my_trip.nom else []
        similar_en_name_trips = [trip.id for trip in base_qs if compare_strings(trip.name, my_trip.name) < 15]
        my_list = list()
        my_list.extend(similar_en_name_trips)
        my_list.extend(similar_fr_name_trips)
        context["same_name_trips"] = base_qs.filter(
            id__in=set(my_list)
        )
        return context

    def form_valid(self, form):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        my_trip.status = 41
        my_trip.verified_by = self.request.user
        my_trip.save()
        return HttpResponseRedirect(reverse("shared_models:close_me_no_refresh"))


class TripSelectFormView(TravelAdminRequiredMixin, CommonPopoutFormView):
    form_class = forms.TripSelectForm
    h1 = gettext_lazy("Please select a trip to re-assign:")
    h3 = gettext_lazy("(You will have a chance to review this action before it is carried out.)")
    submit_text = gettext_lazy("Proceed")

    def test_func(self):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("pk"))
        if my_trip.is_adm_approval_required:
            return in_adm_admin_group(self.request.user)
        else:
            return in_travel_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        trip_a = self.kwargs.get("pk")
        trip_b = form.cleaned_data["trip"]
        return HttpResponseRedirect(reverse("travel:trip_reassign_confirm", kwargs={"trip_a": trip_a, "trip_b": trip_b, }))


class TripReassignConfirmView(TravelAdminRequiredMixin, CommonPopoutFormView):
    template_name = 'travel/trip_reassign_form.html'
    form_class = forms.forms.Form
    width = 1500
    height = 1500
    h1 = gettext_lazy("Please confirm the following:")
    submit_text = gettext_lazy("Confirm")
    field_list = [
        "name",
        "nome",
        'location',
        'lead',
        'start_date',
        'end_date',
        'meeting_url',
        'is_adm_approval_required',
        'status_string|{}'.format("status"),
        'traveller_list|{}'.format("travellers"),
        'requests|{}'.format("linked trip requests"),
    ]

    def test_func(self):
        my_trip = models.Conference.objects.get(pk=self.kwargs.get("trip_a"))
        if my_trip.is_adm_approval_required:
            return in_adm_admin_group(self.request.user)
        else:
            return in_travel_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access", kwargs={
                "message": _("Sorry, only ADMO administrators can verify trips that require ADM approval.")}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_a = models.Conference.objects.get(pk=self.kwargs.get("trip_a"))
        trip_b = models.Conference.objects.get(pk=self.kwargs.get("trip_b"))

        context["trip_a"] = trip_a
        context["trip_b"] = trip_b
        context["trip_list"] = [trip_a, trip_b]

        # start out optimistic
        duplicate_ppl = list()
        # we have to sift through each tr that will be transferred to the new trip and ensure that there is no overlap with the new travellers
        request_users_from_trip_b = [tr.user for tr in trip_b.trip_requests.all() if
                                     tr.user]  # this will be only individual requests and parent group requests
        travellers_from_trip_b = trip_b.traveller_list
        for tr in trip_a.trip_requests.all():
            # if
            if tr.user and tr.user in request_users_from_trip_b:
                duplicate_ppl.append(tr.user)

            # now, depending on whether this request is a group request, our method will change.
            # if TR is a group request, we have to make sure there is no overlap in the travellers
            # but because of the traveller() method, we can just use one approach

            else:
                for traveller in tr.travellers:
                    if traveller in travellers_from_trip_b:
                        duplicate_ppl.append(traveller)

        context["duplicate_ppl"] = duplicate_ppl
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            trip_a = models.Conference.objects.get(pk=self.kwargs.get("trip_a"))
            trip_b = models.Conference.objects.get(pk=self.kwargs.get("trip_b"))

            for tr in trip_a.trip_requests.all():
                tr.trip = trip_b
                tr.save()

            # trip_a.delete()
            return HttpResponseRedirect(reverse("shared_models:close_me"))


class TripReviewListView(TravelAccessRequiredMixin, CommonListView):
    model = models.Conference
    template_name = 'travel/trip_review_list.html'
    home_url_name = "travel:index"
    field_list = [
        {"name": 'status_string|{}'.format(_("status")), "class": "", },
        {"name": 'tname|{}'.format(_("Trip title")), "class": "", },
        {"name": 'location|{}'.format(_("location")), "class": "", },
        {"name": 'dates|{}'.format(_("dates")), "class": "", "width": "180px"},
        {"name": 'number_of_days|{}'.format(_("length (days)")), "class": "center-col", },
        {"name": 'is_adm_approval_required|{}'.format(_("ADM approval required?")), "class": "center-col", },
        {"name": 'total_travellers|{}'.format(_("Total travellers")), "class": "center-col", },
        {"name": 'connected_requests|{}'.format(_("Connected requests")), "class": "center-col", },
        {"name": 'verified_by', "class": "", },
    ]

    def get_queryset(self):
        if self.kwargs.get("which_ones") == "awaiting":
            qs = models.Conference.objects.filter(
                pk__in=[reviewer.trip_id for reviewer in self.request.user.trip_reviewers.filter(status=25)])
        else:
            qs = models.Conference.objects.filter(pk__in=[reviewer.trip_id for reviewer in self.request.user.trip_reviewers.all()])
        return qs

    def get_h1(self):
        if self.kwargs.get("which_ones") == "awaiting":
            h1 = _("Trips Awaiting Your Review")
        else:
            h1 = _("Tagged Trips")
        return h1

    def get_row_object_url_name(self):
        if self.kwargs.get("which_ones") == "awaiting":
            return "travel:trip_reviewer_update"
        else:
            return "travel:trip_detail"


class TripReviewerUpdateView(TravelADMAdminRequiredMixin, CommonUpdateView):
    model = models.TripReviewer
    form_class = forms.ReviewerApprovalForm
    template_name = 'travel/trip_reviewer_approval_form.html'
    back_url = reverse_lazy("travel:trip_review_list")
    cancel_text = _("Cancel")
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Trips Awaiting Your Review"),
                    "url": reverse_lazy("travel:trip_review_list", kwargs={"which_ones": "awaiting"})}

    def test_func(self):
        my_trip = self.get_object().trip
        my_user = self.request.user
        if is_trip_approver(my_user, my_trip):
            return True

    def get_h1(self):
        my_str = _("{}'s Trip Review".format(self.get_object().user.first_name))
        if self.get_object().role == 5:  # if ADM
            my_str += " ({})".format(_("ADM Level Review"))
        return my_str

    def get_submit_text(self):
        if self.get_object().role == 5:  # if ADM
            submit_text = _("Complete the review")
        else:
            submit_text = _("Submit your review")
        return submit_text

    def get_h3(self):
        return self.get_object().trip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conf_field_list"] = conf_field_list
        context["trip"] = self.get_object().trip
        context["reviewer_field_list"] = reviewer_field_list
        context["traveller_field_list"] = traveller_field_list

        context["report_mode"] = True
        trip = self.get_object().trip
        context["is_adm_admin"] = in_adm_admin_group(self.request.user)
        context["is_admin"] = in_travel_admin_group(self.request.user)
        context["is_reviewer"] = self.request.user in [r.user for r in self.get_object().trip.reviewers.all()]

        # if this is the ADM looking at the page, we need to provide more data
        if self.get_object().role == 5:
            # prime a list of trip requests to run by the ADM. This will be a list of travellers (ie. ind TRs and child TRs; not parent records)
            adm_tr_list = list()
            # we need all the trip requests, excluding parents; start out with simple ones

            # get all ind TRs that are pending ADM, pending RDG, denied or accepted
            tr_id_list = [tr.id for tr in trip.trip_requests.filter(is_group_request=False, status__in=[14, 15, 10, 11])]

            # make a list of child requests whose parents are in the same status categories
            child_list = [child_tr.id for parent_tr in trip.trip_requests.filter(is_group_request=True, status__in=[14, 15, 10, 11]) for
                          child_tr in parent_tr.children_requests.all()]
            # extend the list
            tr_id_list.extend(child_list)
            # get a QS from the work done above
            trip_requests = models.TripRequest1.objects.filter(id__in=tr_id_list)

            # go through each trip request
            for tr in trip_requests:
                # the child requests will be set as 'draft', change them to 'pending adm review'
                if tr.parent_request and tr.parent_request.status == 14 and tr.status == 8:
                    tr.status = tr.parent_request.status
                    tr.save()

                # get any adm reviewers of the trip request that is pending; it is important that we only look at parent requests for this
                # hence the use of `smart_reviewer` prop
                my_reviewer = tr.smart_reviewers.get(role=5) if tr.smart_reviewers.filter(role=5, status=1).count() == 1 else None

                # if there is a reviewer and the trip request is a child, we have to actually create a new trip request  reviewer for that child
                if my_reviewer and tr.parent_request:
                    # use get_or_create
                    status = my_reviewer.status
                    my_reviewer, created = models.Reviewer.objects.get_or_create(
                        trip_request=tr,
                        role=my_reviewer.role,
                        user=my_reviewer.user,
                    )
                    if created:
                        my_reviewer.status = status
                        my_reviewer.save()

                adm_tr_list.append({"trip_request": tr, "reviewer": my_reviewer})
            context["adm_tr_list"] = adm_tr_list
            # we need to create a variable that ensures the adm cannot submit her request unless all the trip requests have been actionned
            # basically, we want to make sure there is nothing that has a trip request status of 14

            context["adm_can_submit"] = bool(self.get_object().trip.trip_requests.filter(status=14).count()) is False
        else:
            # otherwise we can always submit the trip
            context["adm_tr_list"] = None
            context["adm_can_submit"] = True
        return context

    def form_valid(self, form):
        my_reviewer = form.save()
        stay_on_page = form.cleaned_data.get("stay_on_page")
        reset = form.cleaned_data.get("reset")

        if not stay_on_page:
            if reset:
                utils.reset_trip_review_process(my_reviewer.trip)
            else:
                # if it was approved, then we change the reviewer status to 'approved'
                my_reviewer.status = 26
                my_reviewer.status_date = timezone.now()
                my_reviewer.save()

            # update any statuses if necessary
            utils.trip_approval_seeker(my_reviewer.trip, self.request)
            return HttpResponseRedirect(reverse("travel:trip_review_list", kwargs={"which_ones": "awaiting"}))

        else:
            my_kwargs = {"pk": my_reviewer.id}
            return HttpResponseRedirect(reverse("travel:trip_reviewer_update", kwargs=my_kwargs))


class SkipTripReviewerUpdateView(TravelAdminRequiredMixin, UpdateView):
    model = models.TripReviewer
    form_class = forms.ReviewerSkipForm
    template_name = 'travel/reviewer_skip_form.html'

    def test_func(self):
        my_trip_request = self.get_object().trip_request
        my_user = self.request.user
        # print(in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request))
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        return context

    def form_valid(self, form):
        # if the form is submitted, that means the admin user has decided to go ahead with the manual skip
        my_reviewer = form.save(commit=False)
        my_reviewer.status = 21
        my_reviewer.status_date = timezone.now()
        my_reviewer.comments = "This step was manually overridden by {} with the following rationale: \n\n {}".format(self.request.user,
                                                                                                                      my_reviewer.comments)

        # now we save the reviewer for real
        my_reviewer.save()

        # update any statuses if necessary
        utils.approval_seeker(my_reviewer.request, False, self.request)

        return HttpResponseRedirect(reverse("shared_models:close_me"))


class TripCancelUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    # TODO: check permissions
    # TODO: cancel related trip requests and email clients
    # TODO: email travellers the change in their statuses

    model = models.Conference
    form_class = forms.TripAdminNotesForm
    template_name = 'travel/form.html'
    submit_text = _("Cancel the trip")
    h1 = _("Do you wish to undo your cancellation request for the following trip?")
    h2 = "<span class='red-font'>" + \
         _("Cancelling this trip will result in all linked requests to be 'cancelled'. "
           "The list of associated trip requests can be viewed below in the trip detail.") + \
         "</span><br><br>" + \
         "<span class='red-font blink-me'>" + \
         _("This action cannot be undone.") + \
         "</span>"
    active_page_name_crumb = _("Cancel Trip")

    # home_url_name = "travel:index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        return context

    def form_valid(self, form):
        my_trip = form.save()
        can_cancel = (my_trip.is_adm_approval_required and in_adm_admin_group(self.request.user)) or \
                     (not my_trip.is_adm_approval_required and in_travel_admin_group(self.request.user))

        # if user is allowed to cancel this request, proceed to do so.
        if can_cancel:
            # cancel any outstanding reviews:
            # but only those with the following statuses: PENDING = 1; QUEUED = 20;
            trip_reviewer_statuses_of_interest = [24, 25, ]
            for r in my_trip.reviewers.filter(status__in=trip_reviewer_statuses_of_interest):
                r.status = 44
                r.save()

            #  CANCEL THE TRIP
            my_trip.status = 43
            my_trip.save()

            # cycle through every trip request associated with this trip and cancel it
            # denied = 10; cancelled = 22; draft = 8;
            tr_statuses_to_skip = [10, 22, 8]
            for tr in my_trip.requests.filter(~Q(status__in=tr_statuses_to_skip)):
                # set status to cancelled = 22
                tr.status = 22
                # update the admin notes
                if tr.admin_notes:
                    tr.admin_notes = f'{my_trip.admin_notes}\n\n{tr.admin_notes}'
                else:
                    tr.admin_notes = f'{my_trip.admin_notes}'
                tr.save()

                # cancel any outstanding reviews:
                # but only those with the following statuses: PENDING = 1; QUEUED = 20;
                tr_reviewer_statuses_of_interest = [1, 20, ]
                for r in tr.reviewers.filter(status__in=tr_reviewer_statuses_of_interest):
                    r.status = 5
                    r.save()

                # send an email to the trip_request owner, if the user has an email address.
                if tr.created_by:
                    email = emails.StatusUpdateEmail(tr, self.request)
                    # # send the email object
                    custom_send_mail(
                        subject=email.subject,
                        html_message=email.message,
                        from_email=email.from_email,
                        recipient_list=email.to_list
                    )

            return HttpResponseRedirect(reverse("travel:trip_detail", kwargs=self.kwargs))
        else:
            return HttpResponseForbidden()


# REPORTS #
###########

class ReportSearchFormView(TravelAdminRequiredMixin, FormView):
    template_name = 'travel/report_search.html'
    form_class = forms.ReportSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        return {
            "fiscal_year": fiscal_year(sap_style=True),
        }

    def form_valid(self, form):
        report = int(form.cleaned_data["report"])
        fy = nz(form.cleaned_data["fiscal_year"], "None")
        region = nz(form.cleaned_data["region"], "None")
        trip = nz(form.cleaned_data["trip"], "None")
        user = nz(form.cleaned_data["user"], "None")
        from_date = nz(form.cleaned_data["from_date"], "None")
        to_date = nz(form.cleaned_data["to_date"], "None")
        adm = nz(form.cleaned_data["adm"], "None")

        if report == 1:
            return HttpResponseRedirect(reverse("travel:export_cfts_list", kwargs={
                'fy': fy,
                'region': region,
                'trip': trip,
                'user': user,
                'from_date': from_date,
                'to_date': to_date,
            }))
        elif report == 2:
            email = form.cleaned_data["traveller"]
            return HttpResponseRedirect(reverse("travel:travel_plan", kwargs={
                'fy': fy,
                'email': email,
            }))

        elif report == 3:
            return HttpResponseRedirect(reverse("travel:export_trip_list", kwargs={
                'fy': fy,
                'region': region,
                'adm': adm,
                'from_date': from_date,
                'to_date': to_date,
            }))

        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("travel:report_search"))


@login_required()
def export_cfts_list(request, fy, region, trip, user, from_date, to_date):
    file_url = reports.generate_cfts_spreadsheet(fiscal_year=fy, region=region, trip=trip, user=user, from_date=from_date, to_date=to_date)
    export_file_name = f'CFTS export {timezone.now().strftime("%Y-%m-%d")}.xlsx'

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        return HttpResponseRedirect(reverse("travel:get_file", args=[file_url.replace("/", "||")]) + f'?blob_name=true;export_file_name={export_file_name}')

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="{export_file_name}"'
            return response
    raise Http404


@login_required()
def export_trip_list(request, fy, region, adm, from_date, to_date):
    site_url = my_envr(request)["SITE_FULL_URL"]
    file_url = reports.generate_trip_list(fiscal_year=fy, region=region, adm=adm, from_date=from_date, to_date=to_date, site_url=site_url)
    export_file_name = f'CTMS trip list {timezone.now().strftime("%Y-%m-%d")}.xlsx'

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        return HttpResponseRedirect(reverse("travel:get_file", args=[file_url.replace("/", "||")]) + f'?blob_name=true;export_file_name={export_file_name}')

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="{export_file_name}"'
            return response
    raise Http404


@login_required()
def export_request_cfts(request, trip=None, trip_request=None):
    file_url = reports.generate_cfts_spreadsheet(trip_request=trip_request, trip=trip)
    export_file_name = f'CFTS export {timezone.now().strftime("%Y-%m-%d")}.xlsx'

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        return HttpResponseRedirect(reverse("travel:get_file", args=[file_url.replace("/", "||")]) + f'?blob_name=true;export_file_name={export_file_name}')

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="CFTS export {}.xlsx"'.format(
                timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404


class TravelPlanPDF(TravelAccessRequiredMixin, PDFTemplateView):
    def get_template_names(self):
        my_object = models.TripRequest1.objects.get(id=self.kwargs['pk'])
        if my_object.travellers.count() > 1:
            template_name = "travel/group_travel_plan.html"
        else:
            template_name = "travel/travel_plan.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = models.TripRequest1.objects.get(id=self.kwargs['pk'])
        context["parent"] = my_object
        context["trip_category_list"] = models.TripCategory.objects.all()

        cost_categories = models.CostCategory.objects.all()
        my_dict = dict()


        my_dict["totals"] = dict()
        my_dict["totals"]["total"] = 0
        for obj in my_object.travellers.all():
            my_dict[obj] = dict()
            for cat in cost_categories:
                if not my_dict["totals"].get(cat):
                    my_dict["totals"][cat] = 0
                cat_amount = obj.costs.filter(cost__cost_category=cat).values("amount_cad").order_by("amount_cad").aggregate(
                    dsum=Sum("amount_cad"))['dsum']
                my_dict[obj][cat] = cat_amount
                my_dict["totals"][cat] += nz(cat_amount, 0)
                my_dict["totals"]["total"] += nz(cat_amount, 0)

        context['my_dict'] = my_dict
        return context


# SETTINGS #
############


class HelpTextHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.HelpText
    success_url = reverse_lazy("travel:manage_help_text")


class HelpTextFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage HelpText"
    queryset = models.HelpText.objects.all()
    formset_class = forms.HelpTextFormset
    success_url = reverse_lazy("travel:manage_help_text")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_help_text"


class CostCategoryHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.CostCategory
    success_url = reverse_lazy("travel:manage_cost_categories")


class CostCategoryFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Cost Category"
    queryset = models.CostCategory.objects.all()
    formset_class = forms.CostCategoryFormset
    success_url = reverse_lazy("travel:manage_cost_categories")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_cost_category"


class CostHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.Cost
    success_url = reverse_lazy("travel:manage_costs")


class CostFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Cost"
    queryset = models.Cost.objects.all()
    formset_class = forms.CostFormset
    success_url = reverse_lazy("travel:manage_costs")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_cost"


#
# class NJCRatesHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
#     model = models.NJCRates
#     success_url = reverse_lazy("travel:manage_njc_rates")


class NJCRatesFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage NJCRates"
    queryset = models.NJCRates.objects.all()
    formset_class = forms.NJCRatesFormset
    success_url = reverse_lazy("travel:manage_njc_rates")
    home_url_name = "travel:index"


class TripCategoryFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Trip Categories"
    queryset = models.TripCategory.objects.all()
    formset_class = forms.TripCategoryFormset
    success_url = reverse_lazy("travel:manage_trip_categories")
    home_url_name = "travel:index"


# class TripCategoryHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
#     model = models.TripCategory
#     success_url = reverse_lazy("travel:manage_trip_categories")


class TripSubcategoryFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Trip Subcategories"
    queryset = models.TripSubcategory.objects.all()
    formset_class = forms.TripSubcategoryFormset
    success_url = reverse_lazy("travel:manage_trip_subcategories")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_trip_subcategory"


class TripSubcategoryHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.TripSubcategory
    success_url = reverse_lazy("travel:manage_trip_subcategories")


class ProcessStepFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Process Steps"
    queryset = models.ProcessStep.objects.all()
    formset_class = forms.ProcessStepFormset
    success_url = reverse_lazy("travel:manage_process_steps")
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_process_step"
    container_class = "container-fluid"


class ProcessStepHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.ProcessStep
    success_url = reverse_lazy("travel:manage_process_steps")


class FAQFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage FAQs"
    queryset = models.FAQ.objects.all()
    formset_class = forms.FAQFormset
    success_url_name = "travel:manage_faqs"
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_faq"
    container_class = "container-fluid"


class FAQHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.FAQ
    success_url = reverse_lazy("travel:manage_faqs")


class OrganizationFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Organizations"
    queryset = shared_models.Organization.objects.filter(is_dfo=True)
    formset_class = forms.OrganizationFormset
    success_url_name = "travel:manage_organizations"
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_organization"
    container_class = "container-fluid"


class OrganizationHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = shared_models.Organization
    success_url = reverse_lazy("travel:manage_organizations")


class RoleFormsetView(TravelAdminRequiredMixin, CommonFormsetView):
    template_name = 'travel/formset.html'
    h1 = "Manage Roles"
    queryset = models.Role.objects.all()
    formset_class = forms.RoleFormset
    success_url_name = "travel:manage_roles"
    home_url_name = "travel:index"
    delete_url_name = "travel:delete_role"


class RoleHardDeleteView(TravelAdminRequiredMixin, CommonHardDeleteView):
    model = models.Role
    success_url = reverse_lazy("travel:manage_roles")


# Reference Materials
class ReferenceMaterialListView(TravelAdminRequiredMixin, CommonListView):
    template_name = "travel/list.html"
    model = models.ReferenceMaterial
    field_list = [
        {"name": "tname|{}".format(gettext_lazy("name")), "class": "", "width": ""},
        {"name": "turl|{}".format(gettext_lazy("URL")), "class": "", "width": ""},
        {"name": "tfile|{}".format(gettext_lazy("File")), "class": "", "width": ""},
        {"name": "created_at", "class": "", "width": ""},
        {"name": "updated_at", "class": "", "width": ""},
    ]
    new_object_url_name = "travel:ref_mat_new"
    row_object_url_name = "travel:ref_mat_edit"
    home_url_name = "travel:index"
    h1 = gettext_lazy("Reference Materials")
    container_class = "container bg-light curvy"


class ReferenceMaterialUpdateView(TravelAdminRequiredMixin, CommonUpdateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("travel:ref_mat_list")}
    template_name = "travel/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"

    def get_delete_url(self):
        return reverse("travel:ref_mat_delete", args=[self.get_object().id])


class ReferenceMaterialCreateView(TravelAdminRequiredMixin, CommonCreateView):
    model = models.ReferenceMaterial
    form_class = forms.ReferenceMaterialForm
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("travel:ref_mat_list")}
    template_name = "travel/form.html"
    is_multipart_form_data = True
    container_class = "container bg-light curvy"


class ReferenceMaterialDeleteView(TravelAdminRequiredMixin, CommonDeleteView):
    model = models.ReferenceMaterial
    success_url = reverse_lazy('travel:ref_mat_list')
    home_url_name = "travel:index"
    parent_crumb = {"title": _("Reference Materials"), "url": reverse_lazy("travel:ref_mat_list")}
    template_name = "travel/confirm_delete.html"
    delete_protection = False
    container_class = "container bg-light curvy"


# Default Reviewer Settings

class DefaultReviewerListView(TravelAdminRequiredMixin, CommonListView):
    model = models.DefaultReviewer
    template_name = 'travel/default_reviewer/default_reviewer_list.html'
    h1 = gettext_lazy("Optional / Special Reviewers")
    h3 = gettext_lazy("Use this module to set the default reviewers that get added to a trip request.")
    new_object_url_name = "travel:default_reviewer_new"
    home_url_name = "travel:index"
    container_class = "container-fluid"
    field_list = [
        {"name": 'user', "class": "", "width": ""},
        {"name": 'sections', "class": "", "width": ""},
        {"name": 'divisions', "class": "", "width": ""},
        {"name": 'branches', "class": "", "width": ""},
        {"name": 'reviewer_roles', "class": "", "width": ""},
    ]


class DefaultReviewerUpdateView(TravelAdminRequiredMixin, UpdateView):
    model = models.DefaultReviewer
    form_class = forms.DefaultReviewerForm
    success_url = reverse_lazy('travel:default_reviewer_list')
    template_name = 'travel/default_reviewer/default_reviewer_form.html'


class DefaultReviewerCreateView(TravelAdminRequiredMixin, CreateView):
    model = models.DefaultReviewer
    form_class = forms.DefaultReviewerForm
    success_url = reverse_lazy('travel:default_reviewer_list')
    template_name = 'travel/default_reviewer/default_reviewer_form.html'


class DefaultReviewerDeleteView(TravelAdminRequiredMixin, DeleteView):
    model = models.DefaultReviewer
    success_url = reverse_lazy('travel:default_reviewer_list')
    success_message = 'The default reviewer was successfully deleted!'
    template_name = 'travel/default_reviewer/default_reviewer_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class UserListView(TravelADMAdminRequiredMixin, CommonFilterView):
    template_name = "travel/user_list.html"
    filterset_class = filters.UserFilter
    home_url_name = "index"
    paginate_by = 25
    h1 = "Travel App User List"
    field_list = [
        {"name": 'first_name', "class": "", "width": ""},
        {"name": 'last_name', "class": "", "width": ""},
        {"name": 'email', "class": "", "width": ""},
        {"name": 'last_login|{}'.format(gettext_lazy("Last login to DM Apps")), "class": "", "width": ""},
    ]
    new_object_url = reverse_lazy("shared_models:user_new")

    def get_queryset(self):
        queryset = User.objects.order_by("first_name", "last_name").annotate(
            search_term=Concat('first_name', Value(""), 'last_name', Value(""), 'email', output_field=TextField())
        )
        if self.kwargs.get("travel"):
            queryset = queryset.filter(groups__in=[33, 36]).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["admin_group"] = Group.objects.get(pk=33)
        context["adm_admin_group"] = Group.objects.get(pk=36)
        return context


@login_required(login_url='/accounts/login/')
@user_passes_test(in_adm_admin_group, login_url='/accounts/denied/')
def toggle_user(request, pk, type):
    my_user = User.objects.get(pk=pk)
    admin_group = Group.objects.get(pk=33)
    adm_admin_group = Group.objects.get(pk=36)
    if type == "admin":
        # if the user is in the admin group, remove them
        if admin_group in my_user.groups.all():
            my_user.groups.remove(admin_group)
        # otherwise add them
        else:
            my_user.groups.add(admin_group)
    elif type == "adm_admin":
        # if the user is in the edit group, remove them
        if adm_admin_group in my_user.groups.all():
            my_user.groups.remove(adm_admin_group)
        # otherwise add them
        else:
            my_user.groups.add(adm_admin_group)

    return HttpResponseRedirect("{}#user_{}".format(request.META.get('HTTP_REFERER'), my_user.id))


# FILES #
#########

class FileCreateView(TravelAccessRequiredMixin, CreateView):
    template_name = "travel/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse("shared_models:close_me"))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        trip_request = models.TripRequest1.objects.get(pk=self.kwargs['trip_request'])
        context["triprequest"] = trip_request
        return context

    def get_initial(self):
        trip_request = models.TripRequest1.objects.get(pk=self.kwargs['trip_request'])

        return {
            'trip_request': trip_request,
        }


class FileUpdateView(TravelAccessRequiredMixin, UpdateView):
    template_name = "travel/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("travel:file_detail", kwargs={"pk": self.object.id})

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


class FileDeleteView(TravelAccessRequiredMixin, DeleteView):
    template_name = "travel/file_confirm_delete.html"
    model = models.File

    def get_success_url(self, **kwargs):
        return reverse_lazy("shared_models:close_me")


# TRAVEL REQUEST COST #
#######################


class TRCostCreateView(LoginRequiredMixin, CreateView):
    model = models.TripRequestCost
    template_name = 'travel/tr_cost_form_popout.html'
    form_class = forms.TripRequestCostForm

    def get_initial(self):
        my_trip_request = models.TripRequest1.objects.get(pk=self.kwargs['trip_request'])
        return {
            'trip_request': my_trip_request,
            # 'number_of_days': my_trip_request.trip.number_of_days,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_trip_request = models.TripRequest1.objects.get(pk=self.kwargs['trip_request'])
        context['triprequest'] = my_trip_request
        return context

    def form_valid(self, form):
        my_object = form.save()
        if my_object.trip_request.trip:
            utils.manage_trip_warning(my_object.trip_request.trip, self.request)
        return HttpResponseRedirect(reverse('shared_models:close_me'))


class TRCostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TripRequestCost
    template_name = 'travel/tr_cost_form_popout.html'
    form_class = forms.TripRequestCostForm

    def form_valid(self, form):
        my_object = form.save()
        if my_object.trip_request.parent_request:
            my_trip = my_object.trip_request.parent_request.trip
        else:
            my_trip = my_object.trip_request.trip
        utils.manage_trip_warning(my_trip, self.request)

        return HttpResponseRedirect(reverse('shared_models:close_me_no_refresh'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def tr_cost_delete(request, pk):
    object = models.TripRequestCost.objects.get(pk=pk)
    if can_modify_request(request.user, object.trip_request.id):
        object.delete()
        messages.success(request, _("The cost has been successfully deleted."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#costs")
    else:
        return HttpResponseRedirect('/accounts/denied/')


def tr_cost_clear(request, trip_request):
    my_trip_request = models.TripRequest1.objects.get(pk=trip_request)
    if can_modify_request(request.user, my_trip_request.id):
        utils.clear_empty_trip_request_costs(my_trip_request)
        messages.success(request, _("All empty costs have been cleared."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#costs")
    else:
        return HttpResponseRedirect('/accounts/denied/')


def tr_cost_populate(request, trip_request):
    my_trip_request = models.TripRequest1.objects.get(pk=trip_request)
    if can_modify_request(request.user, my_trip_request.id):
        utils.populate_trip_request_costs(request, my_trip_request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#costs")
    else:
        return HttpResponseRedirect('/accounts/denied/')
