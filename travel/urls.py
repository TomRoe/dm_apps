from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),

    # EVENT (TRIPS) #
    ##########
    path('trips/', views.TripListView.as_view(), name="trip_list"),
    path('trip/new/', views.TripCreateView.as_view(), name="trip_new"),
    path('trip/<int:pk>/view/', views.TripDetailView.as_view(), name="trip_detail"),
    path('trip/<int:pk>/print/', views.TravelPlanPDF.as_view(), name="trip_print"),
    path('trip/<int:pk>/edit/', views.TripUpdateView.as_view(), name="trip_edit"),
    path('trip/<int:pk>/edit/<str:pop>/', views.TripUpdateView.as_view(), name="trip_edit"),
    path('trip/<int:pk>/delete/', views.TripDeleteView.as_view(), name="trip_delete"),
    path('trip/<int:pk>/delete/pop/<str:pop>/', views.TripDeleteView.as_view(), name="trip_delete"),
    path('trip/<int:pk>/duplicate/', views.TripCloneUpdateView.as_view(), name="duplicate_event"),
    path('trip/<int:pk>/new-child-trip/', views.TripCreateView.as_view(), name="trip_new"),
    path('trip/<int:pk>/clone-duplicate/pop/<str:pop>', views.ChildTripCloneUpdateView.as_view(), name="child_duplicate_event"),

    path('trips/approval/', views.TripApprovalListView.as_view(), name="trip_review_list"),
    path('trips/approval/<str:which_ones>/', views.TripApprovalListView.as_view(), name="trip_review_list"),
    path('trip/<int:pk>/approve/', views.TripApproveUpdateView.as_view(), name="trip_approve"),

    path('trip/<int:pk>/submit/', views.TripSubmitUpdateView.as_view(), name="trip_submit"),

    path('admin/approval/', views.TripAdminApprovalListView.as_view(), name="admin_approval_list"),
    path('admin/<int:pk>/approve/', views.TripAdminApproveUpdateView.as_view(), name="admin_approve"),


    # CONFERENCE #
    ####################
    path('conferences/', views.ConferenceListView.as_view(), name="conf_list"),
    path('conference/new/', views.ConferenceCreateView.as_view(), name="conf_new"),
    path('conference/new/pop/<int:pop>/', views.ConferenceCreateView.as_view(), name="conf_new"),
    path('conference/<int:pk>/view/', views.ConferenceDetailView.as_view(), name="conf_detail"),
    path('conference/<int:pk>/edit/', views.ConferenceUpdateView.as_view(), name="conf_edit"),
    path('conference/<int:pk>/delete/', views.ConferenceDeleteView.as_view(), name="conf_delete"),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/export-cfts-list/year/<int:fy>/user/<int:user>/', views.export_cfts_list, name="export_cfts_list"),
    path('reports/cfts/trip/<int:pk>/', views.export_trip_cfts, name="export_cfts"),
    # path('event/<int:fy>/<str:email>/print/', views.TravelPlanPDF.as_view(), name="travel_plan"),

    # SETTINGS #
    ############
    path('settings/statuses/', views.manage_statuses, name="manage_statuses"),
    path('settings/status/<int:pk>/delete/', views.delete_status, name="delete_status"),

]
