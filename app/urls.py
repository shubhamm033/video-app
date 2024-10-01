from django.urls import path
from . import views

urlpatterns = [
    path("user/create/", views.create_user, name="create_user"),
    path("video/upload/", views.save_video_details, name="save_video_details"),
    path("video/<int:id>/", views.fetch_video_details, name="fetch_video_detils"),
    path("video/watch/", views.watch_video, name="watch_video")

]
