from django.shortcuts import render
from django.views.generic.list import ListView
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Q
from django.db.models import Count
import calendar
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Locations, Incident, FireStation
from fire.forms import FireStationForm, IncidentForm, LocationForm

class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

def map_station(request):
    fireStations = FireStation.objects.values('name', 'latitude', 'longitude')

    for fs in fireStations:
        fs['latitude'] = float(fs['latitude'])
        fs['longitude'] = float(fs['longitude'])

    fireStations_list = list(fireStations)

    context = {
        'fireStations': fireStations_list,
    }

    return render(request, 'map_station.html', context)


def map_incidents(request):
    # Get the city from the request parameters
    city = request.GET.get('city', '')

    
    query = """
        SELECT
            fire_locations.latitude AS latitude,
            fire_locations.longitude AS longitude,
            fire_locations.address AS address,
            fire_incident.severity_level AS severity_level,
            fire_incident.description AS description
        FROM
            fire_incident
        INNER JOIN  
            fire_locations ON fire_incident.location_id = fire_locations.id
        WHERE
            fire_locations.city = %s
    """

    # Execute the SQL query with the city parameter
    with connection.cursor() as cursor:
        cursor.execute(query, [city])
        rows = cursor.fetchall()

    # Prepare data for the templates
    incident_data = []

    for row in rows:
        latitude = row[0]
        longitude = row[1]
        address = row[2]  # Fix here: Assign the correct variable to address
        severity_level = row[3]  # Fix here: Assign the correct variable to severity_level
        description = row[4]  # Fix here: Assign the correct variable to description

        incident_data.append({
            'latitude': latitude,
            'longitude': longitude,
            'address': address,
            'severity_level': severity_level,
            'description': description
        })

    # Get cities for the city dropdown
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT city FROM fire_locations")
        cities = cursor.fetchall()
        cities_list = [city[0] for city in cities]

    context = {
        'incident_data': incident_data,
        'cities': cities_list,
    }

    return render(request, 'map_incident.html', context)


def city_data(request):
    city_name = request.GET.get('city')
    if city_name:
        # Fetch the city's average latitude and longitude
        city_locations = Locations.objects.filter(city=city_name)
        if city_locations.exists():
            city = city_locations.first()
            incidents = Incident.objects.filter(location__city=city_name)
            incident_data = [{
                'latitude': float(incident.location.latitude),
                'longitude': float(incident.location.longitude),
                'address': incident.location.address
            } for incident in incidents]
            data = {
                'latitude': float(city.latitude),
                'longitude': float(city.longitude),
                'incidents': incident_data
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'City not found'}, status=404)
        
def city_incidents(request):
    city = request.GET.get('city', '')
    query = """
        SELECT fire_locations.latitude AS latitude, fire_locations.longitude AS longitude,
        fire_locations.address AS address
        FROM fire_incident
        INNER JOIN fire_locations ON fire_incident.location_id = fire_locations.id
        WHERE fire_locations.city = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [city])
        rows = cursor.fetchall()
        incident_data = []
        for row in rows:
            latitude = row[0]
            longitude = row[1]
            address = row[2]
            incident_data.append({
                'latitude': latitude,
                'longitude': longitude,
                'address': address
            })
    return JsonResponse({'incidents_data': incident_data})








class FireStationListView(ListView):
    model = FireStation
    context_object_name = 'stations'
    template_name = 'fire_station_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query)
            )
        return qs.order_by('id')  

class FireStationCreateView(CreateView):
    model = FireStation
    form_class = FireStationForm
    template_name = 'fire_station_form.html'
    success_url = reverse_lazy('fire_station_list')

class FireStationUpdateView(UpdateView):
    model = FireStation
    form_class = FireStationForm
    template_name = 'fire_station_form.html'
    success_url = reverse_lazy('fire_station_list')


class FireStationDeleteView(DeleteView):
    model = FireStation
    template_name = 'fire_station_confirm_delete.html'
    success_url = reverse_lazy('fire_station_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['station_name'] = self.object.name
        return context











class IncidentListView(ListView):
    model = Incident
    template_name = 'incident_list.html'
    context_object_name = 'incidents'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(location__icontains=query) | Q(description__icontains=query) | Q(severity_level__icontains=query))
        return queryset.order_by('id')  

 
class IncidentCreateView(CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incident_form.html'
    success_url = reverse_lazy('incident_list')

class IncidentUpdateView(UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incident_form.html'
    success_url = reverse_lazy('incident_list')

class IncidentDeleteView(DeleteView):
    model = Incident
    template_name = 'incident_confirm_delete.html'
    success_url = reverse_lazy('incident_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incident_description'] = self.object.description
        return context
    



class LocationListView(ListView):
    model = Locations
    template_name = 'location_list.html'
    context_object_name = 'locations'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(address__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query))
        return queryset.order_by('id')  

class LocationCreateView(CreateView):
    model = Locations
    form_class = LocationForm
    template_name = 'location_form.html'
    success_url = reverse_lazy('location_list')

class LocationUpdateView(UpdateView):
    model = Locations
    form_class = LocationForm
    template_name = 'location_form.html'
    success_url = reverse_lazy('location_list')

class LocationDeleteView(DeleteView):
    model = Locations
    template_name = 'location_confirm_delete.html'
    success_url = reverse_lazy('location_list')



class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super(). get_context_data(**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        pass
    
def PieCountbySeverity(request):
        query = '''
        SELECT severity_level, COUNT(*) as count
        FROM fire_incident
        GROUP BY severity_level
        '''
        data = {}
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        if rows:
# Construct the dictionary with severity level as keys and count as values
            data = {severity: count for severity, count in rows}
        else:
            data = {}
        return JsonResponse(data)


def LineCountbyMonth(request):

    current_year = datetime.now().year

    result = {month: 0 for month in range(1, 13)}

    incidents_per_month = Incident.objects.filter(date_time__year=current_year) \
        .values_list('date_time', flat=True)

    # Counting the number of incidents per month
    for date_time in incidents_per_month:
        month = date_time.month
        result[month] += 1

    # If you want to convert month numbers to month names, you can use a dictionary mapping
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    result_with_month_names = {
        month_names[int(month)]: count for month, count in result.items()
    }

    return JsonResponse(result_with_month_names)


def MultilineIncidentTop3Country(request):

    query = '''
    SELECT
    fl.country,
    strftime('%m', fi.date_time) AS month,
    COUNT(fi.id) AS incident_count
    FROM
    fire_incident fi
    JOIN
    fire_locations fl ON fi.location_id = fl.id
    WHERE
    fl.country IN (
        SELECT
            fl_top.country
        FROM
            fire_incident fi_top
        JOIN
            fire_locations fl_top ON fi_top.location_id = fl_top.id
        WHERE
            strftime('%Y', fi_top.date_time) = strftime('%Y', 'now')
        GROUP BY
            fl_top.country
        ORDER BY
            COUNT(fi_top.id) DESC
        LIMIT 3
    )
    AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
    GROUP BY
    fl.country, month
    ORDER BY
    fl.country, month;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
    rows = cursor.fetchall()

    # Initialize a dictionary to store the result
    result = {}

    # Initialize a set of months from January to December
    months = set(str(i).zfill(2) for i in range(1, 13))

    # Loop through the query results
    for row in rows:
        country = row[0]
    month = row[1]
    total_incidents = row[2]

    # If the country is not in the result dictionary, initialize it with all months set to zero
    if country not in result:
        result[country] = {month: 0 for month in months}

    # Update the incident count for the corresponding month
    result[country][month] = total_incidents

    # Ensure there are always 3 countries in the result
    while len(result) < 3:
    # Placeholder name for missing countries
        missing_country = f"Country {len(result) + 1}"
    result[missing_country] = {month: 0 for month in months}

    for country in result:
     result[country] = dict(sorted(result[country].items()))
    return JsonResponse(result)

def multipleBarbySeverity(request):
    query = '''
    SELECT
        fi.severity_level,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM
        fire_incident fi
    GROUP BY fi.severity_level, month
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = set(str(i).zfill(2) for i in range(1, 13))

    for row in rows:
        level = str(row[0])  # Ensure the severity level is a string
        month = row[1]
        total_incidents = row[2]

        if level not in result:
            result[level] = {month: 0 for month in months}

        result[level][month] = total_incidents

    # Sort months within each severity level
    for level in result:
        result[level] = dict(sorted(result[level].items()))
    return JsonResponse(result)


