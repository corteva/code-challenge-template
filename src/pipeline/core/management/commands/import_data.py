import os
import pandas as pd
from datetime import datetime

from django.core.management.base import BaseCommand

from crop.models import CropData
from weather.models import WeatherData

WEATHER = "weather"
YIELD = "yield"


class Command(BaseCommand):
    # todo: maybe not in core since core is imported from in other places
    help = "Extract phase of pipeline"

    def add_arguments(self, parser):
        parser.add_argument("-w", "--weather", action="store_true", help="Load weather data from the txt files in the wx_data folder")
        parser.add_argument("-y", "--yield", action="store_true", help="Load yield data from the txt files in the yld_data folder")

    def handle(self, *args, **kwargs):
        path = "../../{}/"
        start_time = datetime.now()
        if kwargs.get(WEATHER, False):
            self.stdout.write(self.style.SUCCESS(f"Starting ingestion of weather data from the txt files in the wx_data folder at {start_time}."))
            path = path.format("wx_data")
            self._read_txt_files(path, WEATHER)
        elif kwargs.get(YIELD, False):
            self.stdout.write(self.style.SUCCESS(f"Starting ingestion of weather data from the txt files in the wx_data folder at {start_time}."))
            path = path.format("yld_data")
            self._read_txt_files(path, YIELD)
        else:
            WeatherData.objects.all().delete()
            self.stdout.write(self.style.ERROR(f"Failed start data ingestion. Please specify -w/--weather or -y/--yield after 'import_data' in the command."))
        return

    def _read_txt_files(self, path: str, data_type: str) -> None:
        success_count = 0
        failed_count = 0
        files = os.listdir(path)
        for file in files:
            if file.endswith(".txt"):
                file_name = file[:-4]
                file_path = path + file
                df = pd.read_table(file_path, header=None, names=["date", "max_temp", "min_temp", "precipitation"])
                df["station_id"] = file_name
                df["date"] = df["date"].apply(self._format_date)
                records = df.to_dict('records')
                objs = [WeatherData(**record) for record in records]
                WeatherData.objects.bulk_create(objs)
                print(WeatherData.objects.all().count())
        end_time = datetime.now()
        self.stdout.write(self.style.SUCCESS(
            f"Finished ingestion of data at {end_time}. success_count = {success_count}   failed_count = {failed_count}"))

    def _create_record(self, file_name: str, data_type: str, data: list) -> None:
        if data_type == YIELD:
            CropData.objects.create(year=data[0], corn_yield=data[1])
        elif data_type == WEATHER:
            station_id = file_name
            date = self._format_date(data[0])
            max_temp = self._shift_decimal(float(data[1]), -1)
            min_temp = self._shift_decimal(float(data[2]), -1)
            precipitation = self._shift_decimal(float(data[3]), -1)
            WeatherData.objects.create(station_id=station_id, date=date, max_temp=max_temp, min_temp=min_temp, precipitation=precipitation)

    def _format_date(self, date: str) -> str:
        date = str(date)
        year = date[:4]
        month = date[4:6]
        day = date[6:]
        formatted_date = f"{year}-{month}-{day}"
        return formatted_date
    def _shift_decimal(self, num: float, shift: int) -> float:
        if num == -9999.0:
            return num
        shifted_num = num * 10.0**shift
        return shifted_num



