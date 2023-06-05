from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import *
import folium


# Create your views here.
def calculate_distance_view(request):
	# Initial Values
	distance = None
	destination = None
	obj = get_object_or_404(Measurement, id=1)
	form = MeasurementModelForm(request.POST or None)
	geolocator = Nominatim(user_agent = 'measurements')

	ip_ = get_ip_address(request)
	print(ip_)
	ip = '72.14.207.99'
	country, city, lat, lon = get_geo(ip)

	location = geolocator.geocode(city)

	# Location Coordinate
	l_lat = lat
	l_lon = lon
	pointA = (l_lat, l_lon)

	# Initial Folium Map
	m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)

	#Location Marker
	folium.Marker([l_lat, l_lon], tooltip= 'click here for more', popup= city['city'], icon=folium.Icon(color='red')).add_to(m)



	if form.is_valid():
		instance = form.save(commit=False)
		destination_ = form.cleaned_data.get('destination')
		destination = geolocator.geocode(destination_)

		# Destination Coordinate
		d_lat = destination.latitude
		d_lon = destination.longitude
		pointB = (d_lat, d_lon)

		# Distance Calculation 
		distance = round(geodesic(pointA, pointB).km, 2)

		# Folium Map Modification
		m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start = get_zoom(distance))

		#Location Marker
		folium.Marker([l_lat, l_lon], tooltip= 'click here for more', popup= city['city'], icon=folium.Icon(color='red')).add_to(m)

		#Destination Marker
		folium.Marker([d_lat, d_lon], tooltip= 'click here for more', popup=destination, icon=folium.Icon(color='green', icon= 'cloud')).add_to(m)


		# Draw line between location and destination.
		line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
		m.add_child(line)


		instance.location = location
		instance.distance = distance
		instance.save()

	m = m._repr_html_()


	context = {
		'distance' : distance,
		'destination' : destination,
		'form': form,
		'map': m,
	}

	return render(request, 'measurements/main.html', context)