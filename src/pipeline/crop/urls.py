from django.urls import path

from crop.views import CropListView


urlpatterns = [
    path("yield", CropListView.as_view(), name="crop_list"),
]
