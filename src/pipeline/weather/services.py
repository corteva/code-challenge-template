from django.db.models import Max, Min, Avg, Sum, Subquery, F

from weather.models import WeatherData, Statistics


def generate_years_list():
    min_date = WeatherData.objects.aggregate(Min("date"))
    max_date = WeatherData.objects.aggregate(Max("date"))
    start_year = min_date["date__min"].year
    end_year = max_date["date__max"].year
    total_years = end_year - start_year + 1
    years = list()
    for i in range(total_years):
        years.append(start_year + i)
    return years


def calculate_stats(years: list) -> None:
    # todo: note about freq of loads and analysis then maybe less DB queries
    missing_val = -9999
    usable_max_data = WeatherData.objects.exclude(max_temp=missing_val)
    usable_min_data = WeatherData.objects.exclude(min_temp=missing_val)
    usable_precip_data = WeatherData.objects.exclude(precipitation=missing_val)
    station_ids = set(WeatherData.objects.values_list("station_id", flat=True))
    for station_id in station_ids:
        for year in years:
            print(year)
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


def _get_year(date):
    print(date)
    year = date.year
    print(year)
    return year


def _calculate_avg_max_temp(usable_max_data, station_id, year):
    try:
        print(usable_max_data)
        filtered_data = usable_max_data.filter(station_id=station_id, date__year=year)
        print(filtered_data)
        avg_max_temp = filtered_data.aggregate(Avg("max_temp"))
        print(avg_max_temp)
        return avg_max_temp['max_temp__avg']
    except Exception as ex:
        print(ex)
        return None


def _calculate_avg_min_temp(usable_min_data, station_id, year):
    try:
        filtered_data = usable_min_data.filter(station_id=station_id, date__year=year)
        avg_min_temp = filtered_data.aggregate(Avg("min_temp"))
        return avg_min_temp['min_temp__avg']
    except Exception as ex:
        print(ex)
        return None


def _calculate_total_precip(usable_precip_data, station_id, year):
    try:
        filtered_data = usable_precip_data.filter(station_id=station_id, date__year=year)
        total_precipitation = filtered_data.aggregate(Sum("precipitation"))
        return total_precipitation['precipitation__sum']
    except Exception:
        return None
