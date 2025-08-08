from django.urls import path
from . import views

urlpatterns = [
    path('', views.live_view, name='live_view'),
    path('project_structure/', views.project_structure_view, name='project_structure'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reports/', views.reports, name='reports'),
    path('index/', views.index, name='index'),
    path('video/', views.video_feed, name='video_feed'),
    path('stats/', views.stats_feed, name='stats_feed'),
]