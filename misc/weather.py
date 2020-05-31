import forecastio
from locationutil import location_to_latlong

api_key = ""

latlong = location_to_latlong('erie, colorado')
forecast = forecastio.load_forecast(api_key, latlong[0], latlong[1])

print("===========Currently Data=========")
print(forecast.currently())

print("===========Hourly Data=========")
by_hour = forecast.hourly()
print("Hourly Summary: %s" % by_hour.summary)

for hourly_data_point in by_hour.data:
    print(hourly_data_point)

print("===========Daily Data=========")
by_day = forecast.daily()
print("Daily Summary: %s" % (by_day.summary))

for daily_data_point in by_day.data:
    print(daily_data_point)