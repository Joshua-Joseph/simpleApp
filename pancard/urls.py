from django.urls import path
from pancard import views
urlpatterns = [
    path('home/', views.homepage, name='homeName'),
    # access the laptop camera
    path('video_feed', views.video_feed, name='video_feed'),
    path('result', views.result, name='res'),
]
