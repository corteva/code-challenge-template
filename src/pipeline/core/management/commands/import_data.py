import os
import pandas as pd
from datetime import datetime

from django.core.management.base import BaseCommand

from crop.models import CropData
from weather.models import WeatherData

WEATHER = "weather"
YIELD = "yield"


class Command(BaseCommand):
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        super().__init__()

    # todo: maybe not in core since core is imported from in other places
    help = "Extract phase of pipeline"

    def add_arguments(self, parser):
        parser.add_argument(
            "-w",
            "--weather",
            action="store_true",
            help="Load weather data from the txt files in the wx_data folder",
        )
        parser.add_argument(
            "-y",
            "--yield",
            action="store_true",
            help="Load yield data from the txt files in the yld_data folder",
        )

    def handle(self, *args, **kwargs):
        path = "../../{}/"
        start_time = datetime.now()
        if kwargs.get(WEATHER, False):
            start_msg = f"Starting ingestion of weather data from the txt files in the wx_data folder at {start_time}."
            path = path.format("wx_data")
            self._read_txt_files(path, WEATHER, start_msg)
        elif kwargs.get(YIELD, False):
            start_msg = f"Starting ingestion of yield data from the txt files in the yld_data folder at {start_time}."
            path = path.format("yld_data")
            self._read_txt_files(path, YIELD, start_msg)
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed start data ingestion. Please specify -w/--weather or -y/--yield after 'import_data' in "
                    f"the command."
                )
            )
        return

    def _read_txt_files(self, path: str, data_type: str, start_msg: str) -> None:
        self.stdout.write(self.style.SUCCESS(start_msg))
        files = os.listdir(path)
        for file in files:
            if file.endswith(".txt"):
                file_name = file[:-4]
                file_path = path + file
                if data_type == WEATHER:
                    self.load_weather_data(file_path, file_name)
                else:
                    self.load_yield_data(file_path)
                self.stdout.write(f"Done processing file: {file}")

        end_time = datetime.now()
        end_msg = f"Finished importing data at {end_time}. Records loaded: {self.success_count} Records failed: {self.fail_count}"
        self.stdout.write(self.style.SUCCESS(end_msg))

    def load_weather_data(self, file_path, file_name):
        """
        Pandas dataframes had the quickest performance time in combination with the bulk_create method provided by the
        Django ORM since it combines many creates into 1 underlying sql statement.
        """
        start_count = WeatherData.objects.all().count()
        df = pd.read_table(
            file_path,
            header=None,
            names=["date", "max_temp", "min_temp", "precipitation"],
        )
        df["station_id"] = file_name
        df["date"] = df["date"].apply(self._format_date)
        df["max_temp"] = df["max_temp"].apply(self._shift_decimal_by_one)
        df["min_temp"] = df["min_temp"].apply(self._shift_decimal_by_one)
        df["precipitation"] = df["precipitation"].apply(self._shift_decimal_by_two)
        records = df.to_dict("records")
        objs = [WeatherData(**record) for record in records]
        WeatherData.objects.bulk_create(objs, ignore_conflicts=True)
        curr_count = WeatherData.objects.all().count()
        self._update_counts(records, start_count, curr_count)

    def load_yield_data(self, file_path):
        """
        CropData will have the corn_yield updated if there is already an existing record for that year.
        """
        start_count = CropData.objects.all().count()
        df = pd.read_table(
            file_path,
            header=None,
            names=["year", "corn_yield"],
        )
        records = df.to_dict("records")
        objs = [CropData(**record) for record in records]
        returned_objs = CropData.objects.bulk_update_or_create(
            objs, ["corn_yield"], match_field="year", yield_objects=True
        )

        # returned_objs is a generator with the structure: ([created], [updated])
        returned_objs = list(returned_objs)
        updated_objs = returned_objs[0][1]
        # Lower starting count so that updated records will be included in success count. Even if a record has not
        # changed an update will be performed and that will be considered a successful upsert.
        start_count -= len(updated_objs)
        curr_count = CropData.objects.all().count()
        self._update_counts(records, start_count, curr_count)

    def _format_date(self, date: str) -> str:
        """
        Reformats a date from the txt file formatted as YYYYMMDD to a Django compatible format YYYY-MM-DD.
        Example:
            date = 20220910
            returns 2022-09-10
        """
        date = str(date)
        year = date[:4]
        month = date[4:6]
        day = date[6:]
        formatted_date = f"{year}-{month}-{day}"
        return formatted_date

    def _shift_decimal_by_one(self, num: float) -> float:
        shifted_num = self._shift_decimal(num, -1)
        return round(shifted_num, 1)

    def _shift_decimal_by_two(self, num: float) -> float:
        shifted_num = self._shift_decimal(num, -2)
        return round(shifted_num, 2)

    def _shift_decimal(self, num: float, shift: int) -> float:
        """
        Will move the decimal in 'num' to the right or left by 'shift' places.
        The shift will only be done if the number is not the float representation of a MISSING_VALUE
        Example:
            num = 31.4, shift = -1
            returns 3.14
        """
        if num == -9999.0:
            return num
        shifted_num = num * 10.0**shift
        return shifted_num

    def _update_counts(self, records, start_count, curr_count):
        num_records = len(records)
        num_created = curr_count - start_count
        num_failed = num_records - num_created
        self.success_count += num_created
        self.fail_count += num_failed
