import html2text as html2text
import xlsxwriter as xlsxwriter
from django.conf import settings
from django.db.models import Q, Sum
from django.template.defaultfilters import yesno
from django.utils import timezone

from lib.templatetags.custom_filters import zero2val, repeat
from lib.templatetags.verbose_names import get_field_value, get_verbose_label
from shared_models import models as shared_models
from lib.functions.custom_functions import nz, listrify
from lib.functions.verbose_field_name import verbose_field_name
from . import models
import os


def generate_dougs_spreadsheet(fiscal_year, regions, divisions, sections):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'projects', 'temp')
    target_file = "temp_export.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'projects', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    worksheet1 = workbook.add_worksheet(name="Programs by section")
    worksheet2 = workbook.add_worksheet(name="Projects by section")
    worksheet3 = workbook.add_worksheet(name="Unsubmitted projects")

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'normal',
         "text_wrap": True})
    divider_format = workbook.add_format(
        {'bold': True, 'border': 0, 'bg_color': '#bcc5d4', "align": 'normal',
         "text_wrap": True})
    header_format_centered = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'center',
         "text_wrap": True})
    total_format = workbook.add_format({'bg_color': '#D6D1C0', "align": 'left', "text_wrap": True})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True})
    bold_format = workbook.add_format({"align": 'left', 'bold': True})

    # need to assemble a section list
    ## first look at the sections arg; if not null, we don't need anything else
    if sections != "None":
        section_list = shared_models.Section.objects.filter(id__in=sections.split(","))
    ## next look at the divisions arg; if not null, we don't need anything else
    elif divisions != "None":
        section_list = shared_models.Section.objects.filter(division_id__in=divisions.split(","))
    ## next look at the divisions arg; if not null, we don't need anything else
    elif regions != "None":
        section_list = shared_models.Section.objects.filter(division__branch__region_id__in=regions.split(","))
    else:
        section_list = shared_models.Section.objects.all()

    # If there is no user, it means that this report is being called throught the report_search view (as opposed to my_section view)
    project_list = models.Project.objects.filter(year=fiscal_year, submitted=True, section_head_approved=True)
    project_list = project_list.filter(section__in=section_list)

    # spreadsheet: Programs by section #
    #############################

    # This is too complicated a worksheet. let's create column widths manually
    col_max = [35, 30, 50, 8, 10, 30, 10, 10, 10]
    col_max.extend(repeat("10,", 12)[:-1].split(","))
    for j in range(0, len(col_max)):
        worksheet1.set_column(j, j, width=int(col_max[j]))

    worksheet1.write_row(0, 0, [
        "SCIENCE BRANCH WORKPLANNING - SUMMARY OF INPUTTING WORKPLANS (Projects Submitted and Approved by Section Heads in the Workplanning Application)", ],
                         bold_format)

    worksheet1.write_row(1, 0, [timezone.now().strftime('%Y-%m-%d'), ], bold_format)

    if project_list.count() == 0:
        worksheet1.write_row(2, 0, ["There are no projects on which to report", ], bold_format)
    else:
        # get a project list for the year
        worksheet1.merge_range('j3:l3'.upper(), 'A-Base', header_format_centered)
        worksheet1.merge_range('m3:o3'.upper(), 'B-Base', header_format_centered)
        worksheet1.merge_range('p3:r3'.upper(), 'C-Base', header_format_centered)
        worksheet1.merge_range('s3:u3'.upper(), 'Total', header_format_centered)

        header = [
            "Section",
            "Division",
            "Program",
            "Core / flex",
            "Number of projects",
            "Project leads",
            "Contains projects with more than one program?",
            'Total FTE\n(weeks)',
            'Total OT\n(hours)',
            'Salary\n(in excess of FTE)',
            'O & M\n(including staff)',
            'Capital',
            'Salary\n(in excess of FTE)',
            'O & M\n(including staff)',
            'Capital',
            'Salary\n(in excess of FTE)',
            'O & M\n(including staff)',
            'Capital',
            'Salary\n(in excess of FTE)',
            'O & M\n(including staff)',
            'Capital',
        ]

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100

        worksheet1.write_row(3, 0, header, header_format)

        i = 4
        for s in section_list:
            # get a list of projects..
            project_list = s.projects.filter(year=fiscal_year, submitted=True, section_head_approved=True)

            # get a list of programs..
            program_id_list = []
            for p in project_list:
                if p.programs.count() > 0:
                    program_id_list.extend([program.id for program in p.programs.all()])
            program_list = models.Program2.objects.filter(id__in=program_id_list)
            for program in program_list:

                project_count = project_list.filter(programs=program).count()
                leads = listrify(
                    list(set([str(staff.user) for staff in
                              models.Staff.objects.filter(project__in=project_list.filter(programs=program), lead=True) if staff.user])))
                is_double_count = len(
                    [project for project in project_list.filter(programs=program).all() if project.programs.count() > 1]) > 0

                total_fte = models.Staff.objects.filter(
                    project__in=project_list.filter(programs=program)
                ).order_by("duration_weeks").aggregate(dsum=Sum("duration_weeks"))['dsum']
                total_ot = models.Staff.objects.filter(
                    project__in=project_list.filter(programs=program)
                ).order_by("overtime_hours").aggregate(dsum=Sum("overtime_hours"))['dsum']

                data_row = [
                    s.name,
                    s.division.name,
                    "{} - {}".format(program.national_responsibility_eng, program.regional_program_name_eng),
                    program.get_is_core_display(),
                    project_count,
                    leads,
                    yesno(is_double_count),
                    zero2val(total_fte, None),
                    zero2val(total_ot, None),
                ]
                total_salary = 0
                total_om = 0
                total_capital = 0
                for source in models.FundingSource.objects.filter(id__in=[1, 2, 3]):
                    staff_salary = models.Staff.objects.filter(project__in=project_list.filter(programs=program)).filter(
                        employee_type__exclude_from_rollup=False, employee_type__cost_type=1, funding_source=source
                    ).order_by("cost").aggregate(dsum=Sum("cost"))['dsum']
                    staff_om = models.Staff.objects.filter(project__in=project_list.filter(programs=program)).filter(
                        employee_type__exclude_from_rollup=False, employee_type__cost_type=2, funding_source=source
                    ).order_by("cost").aggregate(dsum=Sum("cost"))['dsum']

                    other_om = models.OMCost.objects.filter(
                        project__in=project_list.filter(programs=program), funding_source=source
                    ).order_by("budget_requested").aggregate(dsum=Sum("budget_requested"))['dsum']

                    capital = models.CapitalCost.objects.filter(
                        project__in=project_list.filter(programs=program), funding_source=source
                    ).order_by("budget_requested").aggregate(dsum=Sum("budget_requested"))['dsum']

                    total_salary += nz(staff_salary, 0)
                    total_om += nz(staff_om, 0) + nz(other_om, 0)
                    total_capital += nz(capital, 0)

                    data_row.extend([
                        zero2val(staff_salary, None),
                        zero2val(nz(staff_om, 0) + nz(other_om, 0), None),
                        zero2val(capital, None),
                    ])
                data_row.extend([
                    zero2val(total_salary, None),
                    zero2val(total_om, None),
                    zero2val(total_capital, None),
                ])

                j = 0

                worksheet1.write_row(i, 0, data_row, normal_format)
                i += 1
            # if there are no projects, don't add a line!
            if s.projects.count() > 0:
                worksheet1.write_row(i, 0, repeat(" ,", len(header) - 1).split(","), divider_format)
                i += 1

    # # set formatting for finances
    # for status in models.Status.objects.all():
    #     worksheet1.conditional_format(4, 9, i, 9,
    #                              {
    #                                  'type': 'cell',
    #                                  'criteria': 'equal to',
    #                                  'value': '"{}"'.format(status.name),
    #                                  'format': workbook.add_format({'bg_color': status.color, }),
    #                              })


    workbook.close()
    return target_url


def generate_master_spreadsheet(fiscal_year, regions, divisions, sections, user=None):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'projects', 'temp')
    target_file = "temp_export.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'projects', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    worksheet1 = workbook.add_worksheet(name="Project List")
    worksheet2 = workbook.add_worksheet(name="FTE List")
    worksheet3 = workbook.add_worksheet(name="Collaborators")
    worksheet4 = workbook.add_worksheet(name="Collaborative Agreements")
    worksheet5 = workbook.add_worksheet(name="O & M")
    worksheet6 = workbook.add_worksheet(name="Capital")
    worksheet7 = workbook.add_worksheet(name="Gs & Cs")

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'normal',
         "text_wrap": True})
    total_format = workbook.add_format({'bg_color': '#D6D1C0', "align": 'left', "text_wrap": True})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True})
    bold_format = workbook.add_format({"align": 'left', 'bold': True})

    # need to assemble a section list
    ## first look at the sections arg; if not null, we don't need anything else
    if sections != "None":
        section_list = shared_models.Section.objects.filter(id__in=sections.split(","))
    ## next look at the divisions arg; if not null, we don't need anything else
    elif divisions != "None":
        section_list = shared_models.Section.objects.filter(division_id__in=divisions.split(","))
    ## next look at the divisions arg; if not null, we don't need anything else
    elif regions != "None":
        section_list = shared_models.Section.objects.filter(division__branch__region_id__in=regions.split(","))
    else:
        section_list = []

        # If there is no user, it means that this report is being called throught the report_search view (as opposed to my_section view)
    if not user:
        project_list = models.Project.objects.filter(year=fiscal_year, section__in=section_list)
        staff_list = models.Staff.objects.filter(project__year=fiscal_year).filter(employee_type=1, project__section__in=section_list)
        collaborator_list = models.Collaborator.objects.filter(project__year=fiscal_year, project__section__in=section_list)
        agreement_list = models.CollaborativeAgreement.objects.filter(project__year=fiscal_year, project__section__in=section_list)
        om_list = models.OMCost.objects.filter(project__year=fiscal_year).filter(budget_requested__gt=0, project__section__in=section_list)
        capital_list = models.CapitalCost.objects.filter(project__year=fiscal_year, project__section__in=section_list)
        gc_list = models.GCCost.objects.filter(project__year=fiscal_year, project__section__in=section_list)
    else:
        project_list = models.Project.objects.filter(year=fiscal_year).filter(section__head_id=user)
        staff_list = models.Staff.objects.filter(project__year=fiscal_year).filter(employee_type=1).filter(
            project__section__head__id=user)
        collaborator_list = models.Collaborator.objects.filter(project__year=fiscal_year).filter(project__section__head__id=user)
        agreement_list = models.CollaborativeAgreement.objects.filter(project__year=fiscal_year).filter(
            project__section__head__id=user)
        om_list = models.OMCost.objects.filter(project__year=fiscal_year).filter(budget_requested__gt=0).filter(
            project__section__head__id=user)
        capital_list = models.CapitalCost.objects.filter(project__year=fiscal_year).filter(project__section__head__id=user)
        gc_list = models.GCCost.objects.filter(project__year=fiscal_year).filter(project__section__head__id=user)

    # spreadsheet: Project List #
    #############################
    if len(project_list) == 0:
        worksheet1.write_row(0, 0, ["There are no projects to report", ], bold_format)
    else:
        # get a project list for the year

        header = [
            "Project ID",
            verbose_field_name(project_list.first(), 'project_title'),
            "Section",
            "Division",
            verbose_field_name(project_list.first(), 'programs'),
            verbose_field_name(project_list.first(), 'tags'),
            "Coding",
            verbose_field_name(project_list.first(), 'status'),
            "Project lead",
            verbose_field_name(project_list.first(), 'is_approved'),
            verbose_field_name(project_list.first(), 'start_date'),
            verbose_field_name(project_list.first(), 'end_date'),
            verbose_field_name(project_list.first(), 'description'),
            verbose_field_name(project_list.first(), 'priorities'),
            verbose_field_name(project_list.first(), 'deliverables'),
            verbose_field_name(project_list.first(), 'data_collection'),
            verbose_field_name(project_list.first(), 'data_sharing'),
            verbose_field_name(project_list.first(), 'data_storage'),
            verbose_field_name(project_list.first(), 'metadata_url'),
            verbose_field_name(project_list.first(), 'regional_dm'),
            verbose_field_name(project_list.first(), 'regional_dm_needs'),
            verbose_field_name(project_list.first(), 'sectional_dm'),
            verbose_field_name(project_list.first(), 'sectional_dm_needs'),
            verbose_field_name(project_list.first(), 'vehicle_needs'),
            verbose_field_name(project_list.first(), 'it_needs'),
            verbose_field_name(project_list.first(), 'chemical_needs'),
            verbose_field_name(project_list.first(), 'ship_needs'),
            'Total FTE (weeks)',
            'Total Salary (in excess of FTE)',
            'Total OT (hours)',
            'Total O & M (including staff)',
            'Total Capital',
            'Total G&Cs',
            verbose_field_name(project_list.first(), 'submitted'),
            verbose_field_name(project_list.first(), 'section_head_approved'),

        ]

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        worksheet1.write_row(0, 0, header, header_format)

        i = 1
        for p in project_list:

            fte_total = 0
            salary_total = 0
            ot_total = 0
            om_total = 0
            gc_total = 0
            capital_total = 0

            # first calc for staff
            for staff in p.staff_members.all():
                # exclude full time employees
                if staff.employee_type.id != 1 or staff.employee_type.id != 6:
                    # if salary
                    if staff.employee_type.cost_type is 1:
                        salary_total += nz(staff.cost, 0)
                    # if o&M
                    elif staff.employee_type.cost_type is 2:
                        om_total += nz(staff.cost, 0)

                # include only FTEs
                fte_total += nz(staff.duration_weeks, 0)

                ot_total += nz(staff.overtime_hours, 0)

            # O&M costs
            for cost in p.om_costs.all():
                om_total += nz(cost.budget_requested, 0)

            # Capital costs
            for cost in p.capital_costs.all():
                capital_total += nz(cost.budget_requested, 0)

            # g&c costs
            for cost in p.gc_costs.all():
                gc_total += nz(cost.budget_requested, 0)

            try:
                budget_code = p.budget_code.code
            except:
                budget_code = "n/a"

            try:
                status = p.status.name
            except:
                status = "n/a"

            try:
                lead = str(
                    ["{} {}".format(lead.user.first_name, lead.user.last_name) for lead in p.staff_members.filter(lead=True)]).replace(
                    "[", "").replace("]", "").replace("'", "").replace('"', "")
            except:
                lead = "n/a"

            try:
                programs = get_field_value(p, "programs")
            except:
                programs = "n/a"

            try:
                tags = get_field_value(p, "tags")
            except:
                tags = "n/a"

            try:
                start = p.start_date.strftime('%Y-%m-%d')
            except:
                start = "n/a"

            try:
                end = p.end_date.strftime('%Y-%m-%d')
            except:
                end = "n/a"

            try:
                division = p.section.division.name
            except:
                division = "MISSING"

            try:
                section = p.section.name
            except:
                section = "MISSING"

            data_row = [
                p.id,
                p.project_title,
                division,
                section,
                programs,
                tags,
                p.coding,
                status,
                lead,
                yesno(p.is_approved),
                start,
                end,
                html2text.html2text(nz(p.description, "")),
                html2text.html2text(nz(p.priorities, "")),
                html2text.html2text(nz(p.deliverables, "")),
                html2text.html2text(nz(p.data_collection, "")),
                html2text.html2text(nz(p.data_sharing, "")),
                html2text.html2text(nz(p.data_storage, "")),
                p.metadata_url,
                p.regional_dm,
                html2text.html2text(nz(p.regional_dm_needs, "")),
                p.sectional_dm,
                html2text.html2text(nz(p.sectional_dm_needs, "")),
                html2text.html2text(nz(p.vehicle_needs, "")),
                html2text.html2text(nz(p.it_needs, "")),
                html2text.html2text(nz(p.chemical_needs, "")),
                html2text.html2text(nz(p.ship_needs, "")),
                fte_total,
                salary_total,
                ot_total,
                om_total,
                capital_total,
                gc_total,
                yesno(p.submitted),
                yesno(p.section_head_approved),
            ]

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

            worksheet1.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            worksheet1.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: FTE List #
    #########################
    if len(staff_list) == 0:
        worksheet2.write_row(0, 0, ["There are no staff to report", ], bold_format)
    else:
        # create a queryset, showing all users and their total hours for FTE

        staff_dict = {}
        for s in staff_list:
            # get the staff members name
            if s.user:
                staff_name = "{}, {}".format(s.user.first_name, s.user.last_name)
            else:
                staff_name = s.name

            try:
                staff_dict[staff_name]
            except KeyError:
                staff_dict[staff_name] = {}
                staff_dict[staff_name]['submitted_approved'] = 0
                staff_dict[staff_name]['submitted_unapproved'] = 0
                staff_dict[staff_name]['unsubmitted'] = 0
                staff_dict[staff_name]['total'] = 0

            if s.project.submitted:
                if s.project.section_head_approved:
                    staff_dict[staff_name]['submitted_approved'] += nz(s.duration_weeks, 0)
                else:
                    staff_dict[staff_name]['submitted_unapproved'] += nz(s.duration_weeks, 0)
            else:
                staff_dict[staff_name]['unsubmitted'] += nz(s.duration_weeks, 0)
            staff_dict[staff_name]['total'] += nz(s.duration_weeks, 0)

        header1 = [
            'FTE Summary in weeks for {}'.format(shared_models.FiscalYear.objects.get(pk=fiscal_year)),
        ]
        worksheet2.write_row(0, 0, header1, bold_format)

        header = [
            'Employee Name',
            'Submitted - Approved',
            'Submitted - Unapproved',
            'Not Submitted',
            'Total',
        ]

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        worksheet2.write_row(1, 0, header, header_format)

        i = 2
        for s in staff_dict:
            data_row = [
                s,
                staff_dict[s]["submitted_approved"],
                staff_dict[s]["submitted_unapproved"],
                staff_dict[s]["unsubmitted"],
                staff_dict[s]["total"],
            ]

            # adjust the width of the columns based on the max string length in each col
            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            worksheet2.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            worksheet2.set_column(j, j, width=col_max[j] * 1.1)

        # TODO: insert conditional formatting regarding the number of hours

        # spreadsheet: collaborator List #
        ##################################
        if len(collaborator_list) == 0:
            worksheet3.write_row(0, 0, ["There are no collaborators to report", ], bold_format)
        else:
            header = [
                "Project Id",
                verbose_field_name(collaborator_list[0], 'name'),
                verbose_field_name(collaborator_list[0], 'type'),
                verbose_field_name(collaborator_list[0], 'critical'),
                verbose_field_name(collaborator_list[0], 'notes'),
            ]

            # create the col_max column to store the length of each header
            # should be a maximum column width to 100
            col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

            worksheet3.write_row(0, 0, header, header_format)

            i = 1
            for item in collaborator_list:
                data_row = [
                    item.project.id,
                    item.name,
                    item.get_type_display(),
                    item.critical,
                    item.notes,
                ]

                # adjust the width of the columns based on the max string length in each col
                j = 0
                for d in data_row:
                    # if new value > stored value... replace stored value
                    if len(str(d)) > col_max[j]:
                        if len(str(d)) < 100:
                            col_max[j] = len(str(d))
                        else:
                            col_max[j] = 100
                    j += 1

                worksheet3.write_row(i, 0, data_row, normal_format)
                i += 1

            for j in range(0, len(col_max)):
                worksheet3.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: agreement List #
    ##################################
    if len(agreement_list) == 0:
        worksheet4.write_row(0, 0, ["There are no agreements to report", ], bold_format)
    else:
        header = [
            "Project Id",
            verbose_field_name(agreement_list[0], 'partner_organization'),
            verbose_field_name(agreement_list[0], 'agreement_title'),
            verbose_field_name(agreement_list[0], 'new_or_existing'),
            verbose_field_name(agreement_list[0], 'notes'),
        ]

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        worksheet4.write_row(0, 0, header, header_format)

        i = 1
        for item in agreement_list:
            data_row = [
                item.project.id,
                item.partner_organization,
                item.agreement_title,
                item.get_new_or_existing_display(),
                item.notes,
            ]

            # adjust the width of the columns based on the max string length in each col
            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            worksheet4.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            worksheet4.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: OM List #
    ########################
    if len(om_list) == 0:
        worksheet5.write_row(0, 0, ["There are no o & m  expenditures to report", ], bold_format)
    else:
        header = [
            "Project Id",
            verbose_field_name(om_list[0], 'om_category'),
            verbose_field_name(om_list[0], 'description'),
            verbose_field_name(om_list[0], 'budget_requested'),
        ]

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        worksheet5.write_row(0, 0, header, header_format)

        i = 1
        for item in om_list:
            data_row = [
                item.project.id,
                str(item.om_category),
                item.description,
                item.budget_requested,
            ]

            # adjust the width of the columns based on the max string length in each col
            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            worksheet5.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            worksheet5.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: Capital List #
    #############################
    if len(capital_list) == 0:
        worksheet6.write_row(0, 0, ["There are no capital expenditures to report", ], bold_format)
    else:

        header = [
            "Project Id",
            verbose_field_name(capital_list[0], 'category'),
            verbose_field_name(capital_list[0], 'description'),
            verbose_field_name(capital_list[0], 'budget_requested'),
        ]

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        worksheet6.write_row(0, 0, header, header_format)

        i = 1
        for item in capital_list:
            data_row = [
                item.project.id,
                item.get_category_display(),
                item.description,
                item.budget_requested,
            ]

            # adjust the width of the columns based on the max string length in each col
            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            worksheet6.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            worksheet6.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: GC List #
    ########################
    if len(gc_list) == 0:
        worksheet7.write_row(0, 0, ["There are no Gs & Cs to report", ], bold_format)
    else:
        header = [
            "Project Id",
            verbose_field_name(gc_list[0], 'recipient_org'),
            verbose_field_name(gc_list[0], 'project_lead'),
            verbose_field_name(gc_list[0], 'proposed_title'),
            verbose_field_name(gc_list[0], 'gc_program'),
            verbose_field_name(gc_list[0], 'budget_requested'),
        ]

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        worksheet7.write_row(0, 0, header, header_format)

        i = 1
        for item in gc_list:
            data_row = [
                item.project.id,
                item.recipient_org,
                item.project_lead,
                item.proposed_title,
                item.gc_program,
                item.budget_requested,
            ]

            # adjust the width of the columns based on the max string length in each col
            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            worksheet7.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            worksheet7.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url


def generate_program_list():
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'projects', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'projects', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting variables
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, })

    # get the program list
    program_list = models.Program2.objects.all()

    field_list = [
        'national_responsibility_eng',
        'national_responsibility_fra',
        'program_inventory',
        'funding_source_and_type',
        'regional_program_name_eng',
        'regional_program_name_fra',
        'examples',
        'is_core',
    ]

    # define the header
    header = [get_verbose_label(program_list.first(), field) for field in field_list]
    header.append('Number of projects tagged')

    title = "Science Program List"
    # define a worksheet
    my_ws = workbook.add_worksheet(name=title)

    i = 3
    for program in program_list:
        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
        my_ws.write(0, 0, title, title_format)
        my_ws.write_row(2, 0, header, header_format)

        data_row = [get_field_value(program, field) for field in field_list]
        data_row.append(program.projects.count())
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

    workbook.close()
    return target_url
