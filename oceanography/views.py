import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse_lazy
from . import models
from . import forms
# Create your views here.

class IndexTemplateView(TemplateView):
    template_name = "oceanography/index.html"

class DocListView(ListView):
    model = models.Doc
    template_name = "oceanography/doc_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class DocCreateView(CreateView):
    model = models.Doc
    template_name = "oceanography/doc_form.html"
    form_class = forms.DocForm
    success_url = reverse_lazy("oceanography:doc_list")

class DocUpdateView(UpdateView):
    model = models.Doc
    template_name = "oceanography/doc_form.html"
    form_class = forms.DocForm
    success_url = reverse_lazy("oceanography:doc_list")

class MissionYearListView(TemplateView):
    template_name = "oceanography/mission_year_list.html"

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)


        # create a reference list of years
        season_list = []
        for item in models.Mission.objects.values("season").distinct():
            season_list.append(item["season"])

        context["season_list"] = season_list
        return context


class MissionListView(ListView):
    template_name = "oceanography/mission_list.html"

    def get_queryset(self):
        return models.Mission.objects.filter(season = self.kwargs["year"])


class MissionDetailView(DetailView):
    template_name = "oceanography/mission_detail.html"
    model = models.Mission

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)

        context["editable"] = False
        return context


class MissionUpdateView(UpdateView):
    template_name = "oceanography/mission_form.html"
    model = models.Mission
    form_class = forms.MissionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:mission_detail", kwargs={"pk":self.object.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)

        context["editable"] = True
        return context


class BottleListView(ListView):
    template_name = "oceanography/bottle_list.html"

    def get_queryset(self):
        return models.Bottle.objects.filter(mission = self.kwargs["mission"])

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)

        context["mission"] = models.Mission.objects.get(id = self.kwargs["mission"])
        context["bottle"] = models.Bottle.objects.first()
        return context

class BottleDetailView(UpdateView):
    template_name = "oceanography/bottle_form.html"
    model = models.Bottle
    form_class = forms.BottleForm

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context


class BottleUpdateView(UpdateView):
    template_name = "oceanography/bottle_form.html"
    model = models.Bottle
    form_class = forms.BottleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:bottle_detail", kwargs={"pk":self.object.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context


# CSVs #
########
def export_mission_csv(request, pk):
    # create instance of mission:
    m = models.Mission.objects.get(pk=pk)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(slugify(m.mission_number))

    writer = csv.writer(response)


    # write the header information
    writer.writerow(['mission_name', m.mission_name])
    writer.writerow(['mission_number', m.mission_number])
    writer.writerow(['vessel_name', m.vessel_name])
    writer.writerow(['chief_scientist', m.chief_scientist])
    writer.writerow(['samplers', m.samplers])
    writer.writerow(['start_date (yyyy-mm-dd)', m.start_date.strftime('%Y-%m-%d')])
    writer.writerow(['end_date (yyyy-mm-dd)', m.end_date.strftime('%Y-%m-%d')])
    writer.writerow(['probe', m.probe])
    writer.writerow(['area_of_operation', m.area_of_operation])
    writer.writerow(['notes', m.notes])
    writer.writerow(['timezone', "UTC"])

    # write the header for the bottle table
    writer.writerow(["",])
    writer.writerow([
    "bottle_uid",
    "station",
    "set",
    "event",
    "date_yyyy_mm_dd",
    "time_hh_mm",
    "sounding_m",
    "bottle_depth_m",
    "temp_c",
    "sal_ppt",
    "ph",
    "lat_DDdd",
    "long_DDdd",
    "ctd_filename",
    "remarks",])

    for b in m.bottles.all():
        writer.writerow(
        [
        b.bottle_uid,
        b.station,
        b.set,
        b.event,
        b.date_time_UTC.strftime('%Y-%m-%d'),
        b.date_time_UTC.strftime('%H:%M'),
        b.sounding_m,
        b.bottle_depth_m,
        b.temp_c,
        b.sal_ppt,
        b.ph,
        b.lat_DDdd,
        b.long_DDdd,
        b.ctd_filename,
        b.remarks,])

    return response


# FILES #
#########

class FileCreateView(CreateView):
    template_name = "oceanography/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("oceanography:mission_detail", kwargs={"pk":object.mission.id}))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context

    def get_initial(self):
        mission = models.Mission.objects.get(pk=self.kwargs['mission'])
        return {'mission': mission}


class FileDetailView(UpdateView):
    template_name = "oceanography/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context


class FileUpdateView(UpdateView):
    template_name = "oceanography/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:mission_detail", kwargs={"pk":self.object.mission.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context

class FileDeleteView(DeleteView):
    template_name = "oceanography/file_confirm_delete.html"
    model = models.File

    def get_success_url(self, **kwargs):
        return reverse_lazy("oceanography:mission_detail", kwargs={"pk":self.object.mission.id})