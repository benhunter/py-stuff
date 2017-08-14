import forecastio
from . import location-util
from .

api_key = ""

location-util.location_to_latlong()

lat = -31.967819
lng = 115.87718
#time = datetime.datetime(2015, 2, 27, 6, 0, 0)

forecast = forecastio.load_forecast(api_key, lat, lng)