import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from crop.factories import CropDataFactory


class YieldViewTests(APITestCase):

    def test_weather_list(self):
        batch_size = 10
        CropDataFactory.create_batch(batch_size)
        url = reverse("crop_list")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), batch_size)
