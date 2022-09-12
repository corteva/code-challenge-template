from datetime import datetime

from django.core.management.base import BaseCommand

from weather.services import generate_years_list, calculate_stats

class Command(BaseCommand):

    help = "Transform phase of pipeline"

    def handle(self, *args, **kwargs):
        start_time = datetime.now()
        start_msg = f"Starting analysis of weather data at {start_time}."
        self.stdout.write(self.style.SUCCESS(start_msg))

        years = generate_years_list()

        if years:
            calculate_stats(years)

            num_years = len(years)
            start_year = years[0]
            end_year = years[num_years - 1]
            end_time = datetime.now()
            end_msg = f"Finished analysis of weather data for years {start_year} - {end_year} at {end_time}."
            self.stdout.write(self.style.SUCCESS(end_msg))
        else:
            end_msg = f"No weather data to analyze"
            self.stdout.write(self.style.ERROR(end_msg))
        return
