import os
import random # todo: remove
from datetime import datetime

from django.db import IntegrityError
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
            self.stdout.write(self.style.ERROR(f"Failed start data ingestion. Please specify -w/--weather or -y/--yield after 'import_data' in the command."))
        return
    
    def _read_txt_files(self, path: str, data_type: str) -> None:
        files = os.listdir(path)
        for file in files:
            if file.endswith(".txt"):
                file_path = path + file
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        data = line.split()
                        try:
                            self._create_record(data_type, data)
                        except IntegrityError as ex:
                            pass
                            # print(ex)
                    f.close()

    def _create_record(self, data_type: str, data: list) -> None:
        if data_type == YIELD:
            CropData.objects.create(year=data[0], corn_yield=data[1])
        elif data_type == WEATHER:
            station_id = random.randint(1, 5) # todo: what is id???
            date = self_format_date(data[0])
            max_temp = self._shift_decimal(data[1], -1)
            min_temp = self._shift_decimal(data[2], -1)
            precipitation = self._shift_decimal(data[3], -1)
            WeatherData.objects.create(station_id=station_id, date=date, max_temp=max_temp, min_temp=min_temp, precipitation=precipitation)

    def _format_date(self, date: str) -> str:
        pass
    def _shift_decimal(self, num: int, shift: int) -> int:
        if num == -9999:
            return num
        shifted_num = num * 10**shift
        return shifted_num



