from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_video, name="upload_video"),
    path("video/<int:video_id>/", views.video_result, name="video_result"),
]