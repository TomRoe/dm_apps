from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'projects'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.IndexTemplateView.as_view(), name="index"),

    # PROJECTS #
    ############
    path('my-list/', views.MyProjectListView.as_view(), name="my_project_list"),
    path('my-section/', views.MySectionListView.as_view(), name="my_section_list"),
    path('my-division/', views.MyDivisionListView.as_view(), name="my_division_list"),
    path('my-branch/', views.MyBranchListView.as_view(), name="my_branch_list"),
    path('all/', views.ProjectListView.as_view(), name="project_list"),
    path('new/', views.ProjectCreateView.as_view(), name="project_new"),
    path('<int:pk>/view/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project/<int:pk>/print/', views.ProjectPrintDetailView.as_view(), name="project_print"),
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name="project_edit"),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name="project_delete"),
    path('project/<int:pk>/submit/', views.ProjectSubmitUpdateView.as_view(), name="project_submit"),
    path('project/<int:pk>/clone/', views.ProjectCloneUpdateView.as_view(), name="project_clone"),
    path('approval/project/<int:pk>/level/<str:level>/', views.ProjectApprovalUpdateView.as_view(), name="project_approval"),

    # STAFF #
    #########
    path('project/<int:project>/staff/new/', views.StaffCreateView.as_view(), name="staff_new"),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name="staff_edit"),
    path('staff/<int:pk>/delete/', views.staff_delete, name="staff_delete"),
    path('staff/<int:pk>/overtime-calculator/', views.OverTimeCalculatorTemplateView.as_view(), name="ot_calc"),

    #  this was used to walk over program to programs
    path('project-formset/', views.temp_formset, name="formset"),
    path('project-program-list/', views.MyTempListView.as_view(), name="my_list"),

    # USER #
    ########
    path('user/new/', views.UserCreateView.as_view(), name="user_new"),

    # Collaborator #
    ################
    path('project/<int:project>/collaborator/new/', views.CollaboratorCreateView.as_view(), name="collab_new"),
    path('collaborator/<int:pk>/edit/', views.CollaboratorUpdateView.as_view(), name="collab_edit"),
    path('collaborator/<int:pk>/delete/', views.collaborator_delete, name="collab_delete"),

    # Collaborative Agreements #
    ############################
    path('project/<int:project>/agreement/new/', views.AgreementCreateView.as_view(), name="agreement_new"),
    path('agreement/<int:pk>/edit/', views.AgreementUpdateView.as_view(), name="agreement_edit"),
    path('agreement/<int:pk>/delete/', views.agreement_delete, name="agreement_delete"),

    # O&M COST #
    ############
    path('project/<int:project>/om-cost/new/', views.OMCostCreateView.as_view(), name="om_new"),
    path('om-cost/<int:pk>/edit/', views.OMCostUpdateView.as_view(), name="om_edit"),
    path('om-cost/<int:pk>/delete/', views.om_cost_delete, name="om_delete"),
    path('om-cost/<int:project>/clear-empty/', views.om_cost_clear, name="om_clear"),
    path('om-cost/<int:project>/populate-all/', views.om_cost_populate, name="om_populate"),

    # CAPITAL COST #
    ################
    path('project/<int:project>/capital-cost/new/', views.CapitalCostCreateView.as_view(), name="capital_new"),
    path('capital-cost/<int:pk>/edit/', views.CapitalCostUpdateView.as_view(), name="capital_edit"),
    path('capital-cost/<int:pk>/delete/', views.capital_cost_delete, name="capital_delete"),

    # G&C COST #
    ############
    path('project/<int:project>/gc-cost/new/', views.GCCostCreateView.as_view(), name="gc_new"),
    path('gc-cost/<int:pk>/edit/', views.GCCostUpdateView.as_view(), name="gc_edit"),
    path('gc-cost/<int:pk>/delete/', views.gc_cost_delete, name="gc_delete"),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path(
        'reports/master-spreadsheet/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
        views.master_spreadsheet, name="report_master"),
    path('reports/project-summary/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFProjectSummaryReport.as_view(), name="pdf_project_summary"),
    path(
        'reports/batch-workplan-export/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
        views.PDFProjectPrintoutReport.as_view(), name="pdf_printout"),

    # this is a special view of the masterlist report that is called from the my_section view
    path('reports/section-head-spreadsheet/fiscal-year/<int:fiscal_year>/user/<int:user>', views.master_spreadsheet, name="report_sh"),

    # path('reports/workplan-summary/fiscal-year/<int:fiscal_year>', views.workplan_summary, name="workplan_summary"),

    # FILES #
    #########
    path('project/<int:project>/file/new/', views.FileCreateView.as_view(), name='file_new'),
    path('project/<int:project>/file/new/status-report/<int:status_report>/', views.FileCreateView.as_view(), name='file_new'),
    path('file/<int:pk>/view/', views.FileDetailView.as_view(), name='file_detail'),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name='file_edit'),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),

    # STATUS REPORT #
    #################
    path('project/<int:project>/status-report/new/', views.StatusReportCreateView.as_view(), name="report_new"),
    path('status-report/<int:pk>/edit/', views.StatusReportUpdateView.as_view(), name="report_edit"),
    path('status-report/<int:pk>/delete/', views.StatusReportDeleteView.as_view(), name="report_delete"),
    path('status-report/<int:pk>/pdf/', views.StatusReportPrintDetailView.as_view(), name="report_print"),

    # MILESTONE #
    #############
    path('project/<int:project>/milestone/new/', views.MilestoneCreateView.as_view(), name="milestone_new"),
    path('milestone/<int:pk>/edit/', views.MilestoneUpdateView.as_view(), name="milestone_edit"),
    path('milestone/<int:pk>/delete/', views.milestone_delete, name="milestone_delete"),

    # MILESTONE UPDATE #
    ####################
    path('milestone-update/<int:pk>/edit/', views.MilestoneUpdateUpdateView.as_view(), name="milestone_update_edit"),

    # SHARED #
    ##########
    path('toggle-funding-source/<str:type>/<int:pk>/', views.toggle_source, name="toggle_source"),

    # SETTINGS #
    ############
    path('settings/funding-source/', views.manage_funding_sources, name="manage_funding_sources"),
    path('settings/funding-source/<int:pk>/delete/', views.delete_funding_source, name="delete_funding_source"),

    path('settings/om-categories/', views.manage_om_cats, name="manage_om_cats"),
    path('settings/om-category/<int:pk>/delete/', views.delete_om_cat, name="delete_om_cat"),

    path('settings/employee-types/', views.manage_employee_types, name="manage_employee_types"),
    path('settings/employee-type/<int:pk>/delete/', views.delete_employee_type, name="delete_employee_type"),

    path('settings/statuses/', views.manage_statuses, name="manage_statuses"),
    path('settings/status/<int:pk>/delete/', views.delete_status, name="delete_status"),

    path('settings/tags/', views.manage_tags, name="manage_tags"),
    path('settings/tag/<int:pk>/delete/', views.delete_tag, name="delete_tag"),

    path('settings/help-text/', views.manage_help_text, name="manage_help_text"),
    path('settings/help-text/<int:pk>/delete/', views.delete_help_text, name="delete_help_text"),

    path('settings/levels/', views.manage_levels, name="manage_levels"),
    path('settings/level/<int:pk>/delete/', views.delete_level, name="delete_level"),

    path('settings/programs/', views.manage_programs, name="manage_programs"),
    path('settings/program/<int:pk>/delete/', views.delete_program, name="delete_program"),

    path('admin-staff-list/', views.AdminStaffListView.as_view(), name="admin_staff_list"),
    path('admin-staff/<int:pk>/edit/<str:qry>/', views.AdminStaffUpdateView.as_view(), name="admin_staff_edit"),
    path('admin-staff/<int:pk>/edit/', views.AdminStaffUpdateView.as_view(), name="admin_staff_edit"),

]
