from django.urls import path

from crop.views import CropListView


urlpatterns = [
    path("", CropListView.as_view(), name="crop_list"),
]
