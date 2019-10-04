import xlsxwriter as xlsxwriter
from django.db.models import Q
from django.template.defaultfilters import yesno
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _

from lib.functions.custom_functions import nz
from lib.templatetags.verbose_names import get_verbose_label
from . import models
import os
from masterlist import models as ml_models


def generate_capacity_spreadsheet(fy, orgs, sectors):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'ihub', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'ihub', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, 'num_format': '$#,##0'})

    # first, filter out the "none" placeholder
    if fy == "None":
        fy = None
    if orgs == "None":
        orgs = None
    if sectors == "None":
        sectors = None

    # build an entry list:
    entry_list = models.Entry.objects.all()

    if fy:
        entry_list = models.Entry.objects.filter(fiscal_year=fy)

    if sectors:
        # we have to refine the queryset to only the selected sectors
        sector_list = [ml_models.Sector.objects.get(pk=int(s)) for s in sectors.split(",")]
        entry_list = entry_list.filter(sectors__in=sector_list)
        # # create the species query object: Q
        # q_objects = Q()  # Create an empty Q object to start with
        # for s in sector_list:
        #     q_objects |= Q(sectors=s)  # 'or' the Q objects together
        # # apply the filter
    if orgs:
        # we have to refine the queryset to only the selected orgs
        org_list = [ml_models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
        entry_list = entry_list.filter(organizations__in=org_list)
        # # create the species query object: Q
        # q_objects = Q()  # Create an empty Q object to start with
        # for o in org_list:
        #     q_objects |= Q(organizations=o)  # 'or' the Q objects together
        # # apply the filter
        # entry_list = entry_list.filter(q_objects)
    else:
        # if no orgs were passed in to the report, we need to make an org list based on the orgs in the entries
        # this org_list will serve as basis for spreadsheet tabs
        org_id_list = list(set([org.id for entry in entry_list for org in entry.organizations.all()]))
        org_list = ml_models.Organization.objects.filter(id__in=org_id_list).order_by("abbrev")

    # define the header
    header = [
        get_verbose_label(entry_list.first(), 'fiscal_year'),
        get_verbose_label(entry_list.first(), 'title'),
        get_verbose_label(entry_list.first(), 'organizations'),
        get_verbose_label(entry_list.first(), 'status'),
        get_verbose_label(entry_list.first(), 'sectors'),
        get_verbose_label(entry_list.first(), 'entry_type'),
        get_verbose_label(entry_list.first(), 'initial_date'),
        get_verbose_label(entry_list.first(), 'regions'),
        get_verbose_label(entry_list.first(), 'funding_needed'),
        get_verbose_label(entry_list.first(), 'funding_purpose'),
        get_verbose_label(entry_list.first(), 'amount_requested'),
        get_verbose_label(entry_list.first(), 'amount_approved'),
        get_verbose_label(entry_list.first(), 'amount_transferred'),
        get_verbose_label(entry_list.first(), 'amount_lapsed'),
        _("Amount outstanding"),
    ]

    # worksheets #
    ##############

    for org in org_list:
        my_ws = workbook.add_worksheet(name=org.abbrev)

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
        my_ws.write(0, 0, str(org), title_format)
        my_ws.write_row(2, 0, header, header_format)

        tot_requested = 0
        tot_approved = 0
        tot_transferred = 0
        tot_lapsed = 0
        tot_outstanding = 0
        i = 3
        for e in entry_list.filter(organizations=org):

            if e.organizations.count() > 0:
                orgs = str([str(obj) for obj in e.organizations.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"',
                                                                                                                                   "")
            else:
                orgs = None

            if e.sectors.count() > 0:
                sectors = str([str(obj) for obj in e.sectors.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            else:
                sectors = None

            if e.regions.count() > 0:
                regions = str([str(obj) for obj in e.regions.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            else:
                regions = None

            data_row = [
                e.fiscal_year,
                e.title,
                orgs,
                str(e.status),
                sectors,
                str(e.entry_type),
                e.initial_date.strftime("%Y-%m-%d"),
                regions,
                yesno(e.funding_needed),
                nz(str(e.funding_purpose), ""),
                nz(e.amount_requested, 0),
                nz(e.amount_approved, 0),
                nz(e.amount_transferred, 0),
                nz(e.amount_lapsed, 0),
                nz(e.amount_outstanding, 0),
            ]

            tot_requested += nz(e.amount_requested, 0)
            tot_approved += nz(e.amount_approved, 0)
            tot_transferred += nz(e.amount_transferred, 0)
            tot_lapsed += nz(e.amount_lapsed, 0)
            tot_outstanding += nz(e.amount_outstanding, 0)

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            my_ws.write_row(i, 0, data_row, normal_format)
            i += 1

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

        # set formatting on currency columns
        # my_ws.set_column(first_col=10, last_col=10, cell_format=money_format)
        # my_ws.set_column(header.index("Funding requested"), header.index("Funding requested"), cell_format=money_format)
        # my_ws.set_column(header.index("Funding approved"), header.index("Funding approved"), cell_format=money_format)
        # my_ws.set_column(header.index("Amount transferred"), header.index("Amount transferred"), cell_format=money_format)
        # my_ws.set_column(header.index("Amount lapsed"), header.index("Amount lapsed"), cell_format=money_format)
        # my_ws.set_column(header.index("Amount outstanding"), header.index("Amount outstanding"), cell_format=money_format)

        # sum all the currency columns
        total_row = [
            _("GRAND TOTAL:"),
            tot_requested,
            tot_approved,
            tot_transferred,
            tot_lapsed,
            tot_outstanding,
        ]
        print(header)
        my_ws.write_row(i + 2, header.index(_("Funding requested")) - 1, total_row, total_format)

        # set formatting for status
        for status in models.Status.objects.all():
            my_ws.conditional_format(0, header.index(_("status").title()), i, header.index(_("status").title()),
                                     {
                                         'type': 'cell',
                                         'criteria': 'equal to',
                                         'value': '"{}"'.format(status.name),
                                         'format': workbook.add_format({'bg_color': status.color, }),
                                     })

        # set formatting for entry type
        for entry_type in models.EntryType.objects.all():
            my_ws.conditional_format(0, header.index(_("Entry Type").title()), i, header.index(_("Entry Type").title()),
                                     {
                                         'type': 'cell',
                                         'criteria': 'equal to',
                                         'value': '"{}"'.format(entry_type.name),
                                         'format': workbook.add_format({'bg_color': entry_type.color, }),
                                     })

    workbook.close()
    return target_url


def generate_summary_spreadsheet(fy, orgs, sectors):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'ihub', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'ihub', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, 'num_format': '$#,##0'})

    # first, filter out the "none" placeholder
    if fy == "None":
        fy = None
    if orgs == "None":
        orgs = None
    if sectors == "None":
        sectors = None

    # get an entry list for the fiscal year (if any)
    if fy:
        entry_list = models.Entry.objects.filter(fiscal_year=fy)
        if sectors:
            # we have to refine the queryset to only the selected sectors
            sector_list = [ml_models.Sector.objects.get(pk=int(s)) for s in sectors.split(",")]
            # create the species query object: Q
            q_objects = Q()  # Create an empty Q object to start with
            for s in sector_list:
                q_objects |= Q(sectors=s)  # 'or' the Q objects together
            # apply the filter
            entry_list = entry_list.filter(q_objects)
        if orgs:
            # we have to refine the queryset to only the selected orgs
            org_list = [ml_models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
            # create the species query object: Q
            q_objects = Q()  # Create an empty Q object to start with
            for o in org_list:
                q_objects |= Q(organizations=o)  # 'or' the Q objects together
            # apply the filter
            entry_list = entry_list.filter(q_objects)

    else:
        entry_list = models.Entry.objects.all()
        if sectors:
            # we have to refine the queryset to only the selected sectors
            sector_list = [ml_models.Sector.objects.get(pk=int(s)) for s in sectors.split(",")]
            # create the species query object: Q
            q_objects = Q()  # Create an empty Q object to start with
            for s in sector_list:
                q_objects |= Q(sectors=s)  # 'or' the Q objects together
            # apply the filter
            entry_list = entry_list.filter(q_objects)
        if orgs:
            # we have to refine the queryset to only the selected orgs
            org_list = [ml_models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
            # create the species query object: Q
            q_objects = Q()  # Create an empty Q object to start with
            for o in org_list:
                q_objects |= Q(organizations=o)  # 'or' the Q objects together
            # apply the filter
            entry_list = entry_list.filter(q_objects)

    # define the header
    header = [
        get_verbose_label(entry_list.first(), 'fiscal_year'),
        get_verbose_label(entry_list.first(), 'title'),
        get_verbose_label(entry_list.first(), 'organizations'),
        get_verbose_label(entry_list.first(), 'status'),
        get_verbose_label(entry_list.first(), 'sectors'),
        get_verbose_label(entry_list.first(), 'entry_type'),
        get_verbose_label(entry_list.first(), 'initial_date'),
        get_verbose_label(entry_list.first(), 'regions'),
        _("DFO Contacts"),
        _("Notes"),
        get_verbose_label(entry_list.first(), 'funding_needed'),
        get_verbose_label(entry_list.first(), 'funding_purpose'),
        get_verbose_label(entry_list.first(), 'amount_requested'),
        get_verbose_label(entry_list.first(), 'amount_approved'),
        get_verbose_label(entry_list.first(), 'amount_transferred'),
        get_verbose_label(entry_list.first(), 'amount_lapsed'),
        _("Amount outstanding"),
    ]

    # worksheets #
    ##############

    # each org should be represented on a separate worksheet
    # therefore determine an appropriate org list

    # based on the resulting query, reconstruct the org list
    org_list = list(set([org for entry in entry_list for org in entry.organizations.all()]))

    # create a queryset
    if len(org_list) > 0:
        # create the species query object: Q
        q_objects = Q()  # Create an empty Q object to start with
        for o in org_list:
            q_objects |= Q(pk=o.id)  # 'or' the Q objects together
        # apply the filter
        org_list = ml_models.Organization.objects.filter(q_objects).order_by("abbrev")

    for org in org_list:
        my_ws = workbook.add_worksheet(name=org.abbrev)

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
        my_ws.write(0, 0, str(org), title_format)
        my_ws.write_row(2, 0, header, header_format)

        tot_requested = 0
        tot_approved = 0
        tot_transferred = 0
        tot_lapsed = 0
        tot_outstanding = 0
        i = 3
        for e in entry_list.filter(organizations=org):

            if e.organizations.count() > 0:
                orgs = str([str(obj) for obj in e.organizations.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"',
                                                                                                                                   "").replace(
                    ', ', "\n")
            else:
                orgs = None

            if e.people.count() > 0:
                people = str(["{} - {} ({})".format(obj.get_role_display(), obj, obj.organization) for obj in e.people.all()]).replace(
                    "[", "").replace("]", "").replace("'", "").replace('"', "").replace(', ', "\n")
            else:
                people = None

            if e.notes.count() > 0:
                notes = ""
                count = 0
                max_count = e.notes.count()
                for obj in e.notes.all():
                    notes += "{} - {} [STATUS: {}] (Created by {} {} on {})\n".format(
                        obj.get_type_display().upper(),
                        obj.note,
                        obj.status,
                        obj.author.first_name,
                        obj.author.last_name,
                        obj.date.strftime("%Y-%m-%d"),
                    )
                    if not count == max_count:
                        notes += "\n"

            else:
                notes = None

            if e.sectors.count() > 0:
                sectors = str([str(obj) for obj in e.sectors.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"',
                                                                                                                                "").replace(
                    ', ', "\n")
            else:
                sectors = None

            if e.regions.count() > 0:
                regions = str([str(obj) for obj in e.regions.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            else:
                regions = None

            data_row = [
                e.fiscal_year,
                e.title,
                orgs,
                str(e.status),
                sectors,
                str(e.entry_type),
                e.initial_date.strftime("%Y-%m-%d"),
                regions,
                people,
                notes,
                yesno(e.funding_needed),
                nz(str(e.funding_purpose), ""),
                nz(e.amount_requested, 0),
                nz(e.amount_approved, 0),
                nz(e.amount_transferred, 0),
                nz(e.amount_lapsed, 0),
                nz(e.amount_outstanding, 0),
            ]

            tot_requested += nz(e.amount_requested, 0)
            tot_approved += nz(e.amount_approved, 0)
            tot_transferred += nz(e.amount_transferred, 0)
            tot_lapsed += nz(e.amount_lapsed, 0)
            tot_outstanding += nz(e.amount_outstanding, 0)

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 75:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 75
                j += 1

            my_ws.write_row(i, 0, data_row, normal_format)
            i += 1

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

        # set formatting on currency columns
        # my_ws.set_column(first_col=10, last_col=10, cell_format=money_format)
        # my_ws.set_column(header.index("Funding requested"), header.index("Funding requested"), cell_format=money_format)
        # my_ws.set_column(header.index("Funding approved"), header.index("Funding approved"), cell_format=money_format)
        # my_ws.set_column(header.index("Amount transferred"), header.index("Amount transferred"), cell_format=money_format)
        # my_ws.set_column(header.index("Amount lapsed"), header.index("Amount lapsed"), cell_format=money_format)
        # my_ws.set_column(header.index("Amount outstanding"), header.index("Amount outstanding"), cell_format=money_format)

        # sum all the currency columns
        total_row = [
            _("GRAND TOTAL:"),
            tot_requested,
            tot_approved,
            tot_transferred,
            tot_lapsed,
            tot_outstanding,
        ]
        my_ws.write_row(i + 2, header.index(_("Funding requested")) - 1, total_row, total_format)

        # set formatting for status
        for status in models.Status.objects.all():
            my_ws.conditional_format(0, header.index(_("status").title()), i, header.index(_("status").title()),
                                     {
                                         'type': 'cell',
                                         'criteria': 'equal to',
                                         'value': '"{}"'.format(status.name),
                                         'format': workbook.add_format({'bg_color': status.color, }),
                                     })

        # set formatting for entry type
        for entry_type in models.EntryType.objects.all():
            my_ws.conditional_format(0, header.index(_("Entry Type").title()), i, header.index(_("Entry Type").title()),
                                     {
                                         'type': 'cell',
                                         'criteria': 'equal to',
                                         'value': '"{}"'.format(entry_type.name),
                                         'format': workbook.add_format({'bg_color': entry_type.color, }),
                                     })

    workbook.close()
    return target_url
