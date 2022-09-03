from django.db.models import Max, Min, Avg, Sum

from weather.models import WeatherData, Statistics


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
            avg_max_temp = _calculate_avg_max_temp(usable_max_data, station_id, year)
            avg_min_temp = _calculate_avg_min_temp(usable_min_data, station_id, year)
            total_precipitation = _calculate_total_precip(
                usable_precip_data, station_id, year
            )
            Statistics.objects.create(
                station_id=station_id,
                year=year,
                avg_max_temp=avg_max_temp,
                avg_min_temp=avg_min_temp,
                total_precipitation=total_precipitation,
            )


def _calculate_avg_max_temp(usable_max_data, station_id, year):
    try:
        filtered_data = usable_max_data.filter(station_id=station_id, year=year)
        avg_max_temp = filtered_data.aggregate(Avg("max_temp"))
        return avg_max_temp
    except Exception:
        return None


def _calculate_avg_min_temp(usable_min_data, station_id, year):
    try:
        filtered_data = usable_min_data.filter(station_id=station_id, year=year)
        avg_min_temp = filtered_data.aggregate(Avg("min_temp"))
        return avg_min_temp
    except Exception:
        return None


def _calculate_total_precip(usable_precip_data, station_id, year):
    try:
        filtered_data = usable_precip_data.filter(station_id=station_id, year=year)
        total_precipitation = filtered_data.aggregate(Sum("precipitation"))
        return total_precipitation
    except Exception:
        return None
