import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class WeatherViewTests(APITestCase):
    def setUp(self):
        django.setup()

    def test_weather_list(self):
        url = reverse("weather_list")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
