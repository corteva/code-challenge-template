from django.db.models import Max, Min

from weather.models import WeatherData


def generate_years_list():
    min_date = WeatherData.objects.aggregate(Min("date"))
    max_date = WeatherData.objects.aggregate(Max("date"))
    start_year = int(min_date["date__min"][:4])
    end_year = int(max_date["date__max"][:4])
    total_years = end_year - start_year + 1
    years = list()
    for i in range(total_years):
        years.append(start_year + i)
    return years


def calculate_stats(years: list):
    # todo: note about freq of loads and analysis then maybe less DB queries
    missing_val = -9999
    usable_max_data = WeatherData.objects.exclude(max_temp=missing_val)
    usable_min_data = WeatherData.objects.exclude(min_temp=missing_val)
    usable_precip_data = WeatherData.objects.exclude(precipitation=missing_val)
    station_ids = WeatherData.objects.values_list("station_id").distinct()
    for station_id in station_ids:
        for year in years:
            pass
