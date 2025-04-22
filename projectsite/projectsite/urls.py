from django.contrib import admin
from django.urls import path
from fire import views
from fire.views import HomePageView, ChartView, PieCountbySeverity, LineCountbyMonth, MultilineIncidentTop3Country, multipleBarbySeverity, FireStationListView, FireStationCreateView, FireStationUpdateView, FireStationDeleteView, IncidentListView, IncidentCreateView, IncidentUpdateView, IncidentDeleteView, LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard_chart', ChartView.as_view(), name='dashboard-chart'),
    path('chart/', PieCountbySeverity, name='chart'),
    path('lineChart/', LineCountbyMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stations', views.map_station, name='map-station'),
    path('incidents', views.map_incidents, name='map-incidents'),
    path('fire-stations/', FireStationListView.as_view(), name='fire_station_list'),
    path('city_data/', views.city_data, name='city_data'),
    path('fire-stations/new/', FireStationCreateView.as_view(), name='fire_station_create'),
    path('fire-stations/<int:pk>/edit/', FireStationUpdateView.as_view(), name='fire_station_update'),
    path('fire-stations/<int:pk>/delete/', FireStationDeleteView.as_view(), name='fire_station_delete'),
    path('incidents/', IncidentListView.as_view(), name='incident_list'),
    path('incidents/add/', IncidentCreateView.as_view(), name='incident_create'),
    path('incidents/<int:pk>/edit/', IncidentUpdateView.as_view(), name='incident_update'),
    path('incidents/<int:pk>/delete/', IncidentDeleteView.as_view(), name='incident_delete'),
    path('locations/', LocationListView.as_view(), name='location_list'),
    path('locations/add/', LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/edit/', LocationUpdateView.as_view(), name='location_update'),
    path('locations/<int:pk>/delete/', LocationDeleteView.as_view(), name='location_delete'),
]
