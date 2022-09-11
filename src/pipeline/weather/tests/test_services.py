import pytest
from datetime import date

from core.constants import MISSING_VALUE

from weather.factories import WeatherDataFactory
from weather.models import Statistics
from weather.services import generate_years_list, calculate_stats

@pytest.mark.django_db
class TestWeatherServices:

    @pytest.mark.parametrize("start_year, end_year", ((1985, 1985), (1985, 1986), (1985, 2014)))
    def test_generate_years_list(self, start_year, end_year):
        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"
        WeatherDataFactory.create(date=date.fromisoformat(start_date))
        WeatherDataFactory.create(date=date.fromisoformat(end_date))
        expected_num_years = end_year - start_year + 1

        returned_years = generate_years_list()

        assert len(returned_years) == expected_num_years
        assert returned_years[0] == start_year
        assert returned_years[expected_num_years - 1] == end_year
        for i in range(expected_num_years - 1):
            assert returned_years[i] + 1 == returned_years[i + 1]
            
    def test_calculate_stats(self):
        batch_size = 5
        year_1 = 1999
        year_2 = 2000
        year_3 = 2001
        years = [year_1, year_2, year_3]
        date_1 = f"{year_1}-02-03"
        date_2 = f"{year_2}-10-10"
        date_3 = f"{year_3}-12-20"
        station_id_1 = "USC12345"
        station_id_2 = "USC67890"
        
        dataset_1 = WeatherDataFactory.create_batch(batch_size, station_id=station_id_1, date=date.fromisoformat(date_1))
        dataset_2 = WeatherDataFactory.create_batch(batch_size, station_id=station_id_1, date=date.fromisoformat(date_2))
        dataset_3 = WeatherDataFactory.create_batch(batch_size, station_id=station_id_2, date=date.fromisoformat(date_1))
        dataset_4 = WeatherDataFactory.create_batch(batch_size, station_id=station_id_2, date=date.fromisoformat(date_2))
        WeatherDataFactory.create(station_id=station_id_1, date=date.fromisoformat(date_1), max_temp=MISSING_VALUE, min_temp=MISSING_VALUE, precipitation=MISSING_VALUE)
        WeatherDataFactory.create(station_id=station_id_1, date=date.fromisoformat(date_3), max_temp=MISSING_VALUE, min_temp=MISSING_VALUE, precipitation=MISSING_VALUE)
        datasets = [dataset_1, dataset_2, dataset_3, dataset_4]

        calculate_stats(years)
        
        for dataset in datasets:
            record = dataset[0]
            year = record.date.year
            station_id = record.station_id
            avg_max_temp, avg_min_temp, total_precipitation = self._calculate_expected_stats(dataset, batch_size)
            statistics = Statistics.objects.get(station_id=station_id, year=year)
            assert avg_max_temp == statistics.avg_max_temp
            assert avg_min_temp == statistics.avg_min_temp
            assert total_precipitation == statistics.total_precipitation

        null_stat = Statistics.objects.get(station_id=station_id_1, year=year_3)
        assert not null_stat.avg_max_temp
        assert not null_stat.avg_min_temp
        assert not null_stat.total_precipitation

    def _calculate_expected_stats(self, dataset, batch_size):
        total_max_temp = 0
        total_min_temp = 0
        total_precipitation = 0

        for record in dataset:
            total_max_temp += record.max_temp
            total_min_temp += record.min_temp
            total_precipitation += record.precipitation

        avg_max_temp = total_max_temp / batch_size
        avg_min_temp = total_min_temp / batch_size

        return avg_max_temp, avg_min_temp, total_precipitation

        
        
        
        
        
