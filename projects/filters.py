from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext as _
from shared_models import models as shared_models
import django_filters
from . import views


class ProjectFilter(django_filters.FilterSet):
    project_title = django_filters.CharFilter(field_name='project_title', lookup_expr='icontains')
    fiscal_year = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact')
    region = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"), lookup_expr='exact')
    division = django_filters.ChoiceFilter(field_name='section__division', lookup_expr='exact', label=_("Division"))
    section = django_filters.ChoiceFilter(field_name='section', lookup_expr='exact', label=_("Section"))
    submitted = django_filters.ChoiceFilter(field_name='submitted', lookup_expr='exact', label=_("Submitted?"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_choices = views.get_region_choices()
        division_choices = views.get_division_choices()
        section_choices = views.get_section_choices()
        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all()]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]

        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices)
        self.filters['submitted'] = django_filters.ChoiceFilter(field_name='submitted', lookup_expr='exact', choices=yes_no_choices)
        self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                              lookup_expr='exact', choices=section_choices)
        self.filters['region'] = django_filters.ChoiceFilter(field_name="section__division__branch__region", label=_("Region"),
                                                              lookup_expr='exact', choices=region_choices)
        self.filters['division'] = django_filters.ChoiceFilter(field_name="section__division", label=_("Division"),
                                                             lookup_expr='exact', choices=division_choices)
        # self.filters['division'] = django_filters.ChoiceFilter(field_name='section__division', lookup_expr='exact', choices=div_choices)

        try:
            # if there is a filter on region, filter the division and section filter accordingly
            if self.data["region"] != "":
                my_region_id = int(self.data["region"])
                division_choices = [my_set for my_set in views.get_division_choices() if
                                    shared_models.Division.objects.get(pk=my_set[0]).branch.region_id == my_region_id]
                self.filters['division'] = django_filters.ChoiceFilter(field_name="section__division", label=_("Division"),
                                                                       lookup_expr='exact', choices=division_choices)

                section_choices = [my_set for my_set in views.get_section_choices() if
                                    shared_models.Section.objects.get(pk=my_set[0]).division.branch.region_id == my_region_id]
                self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                                      lookup_expr='exact', choices=section_choices)

            # if there is a filter on division, filter the section filter accordingly
            if self.data["division"] != "":
                my_division_id = int(self.data["division"])

                section_choices = [my_set for my_set in views.get_section_choices() if
                                   shared_models.Section.objects.get(pk=my_set[0]).division_id == my_division_id]
                self.filters['section'] = django_filters.ChoiceFilter(field_name="section", label=_("Section"),
                                                                      lookup_expr='exact', choices=section_choices)

        except KeyError:
            print('no data in filter')



class MySectionFilter(django_filters.FilterSet):
    fiscal_year = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact')
    project_title = django_filters.CharFilter(field_name='project_title', lookup_expr='icontains')
    staff = django_filters.ChoiceFilter(field_name='staff_members__user', lookup_expr='exact', label="Staff member")
    submitted = django_filters.ChoiceFilter(field_name='submitted', lookup_expr='exact', label="Submitted?")
    approved = django_filters.ChoiceFilter(field_name='section_head_approved', lookup_expr='exact', label="Approved by me?")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all()]
        user_choices = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in User.objects.all().order_by("last_name", "first_name")]
        yes_no_choices = [(True, "Yes"), (False, "No"), ]

        self.filters['fiscal_year'] = django_filters.ChoiceFilter(field_name='year', lookup_expr='exact', choices=fy_choices)
        self.filters['staff'] = django_filters.ChoiceFilter(field_name='staff_members__user', lookup_expr='exact', choices=user_choices)
        self.filters['submitted'] = django_filters.ChoiceFilter(field_name='submitted', lookup_expr='exact', choices=yes_no_choices)
        self.filters['is_approved'] = django_filters.ChoiceFilter(field_name='is_approved', lookup_expr='exact', choices=yes_no_choices)
