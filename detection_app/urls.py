from django.urls import path
from . import views

urlpatterns = [
    path('', views.live_view, name='live_view'),
    path('reports/', views.reports, name='reports'),
    path('index/', views.index, name='index'),
    path('video/', views.video_feed, name='video_feed'),
    path('stats/', views.stats_feed, name='stats_feed'),
]