import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from weather.factories import WeatherDataFactory, StatisticsFactory


class WeatherViewTests(APITestCase):
    def test_weather_list(self):
        batch_size = 10
        WeatherDataFactory.create_batch(batch_size)
        url = reverse("weather_list")
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == batch_size

    def test_statistics_list(self):
        batch_size = 10
        StatisticsFactory.create_batch(batch_size)
        url = reverse("stats_list")
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == batch_size
