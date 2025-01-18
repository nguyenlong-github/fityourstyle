from django.urls import path

from . import views

app_name = 'myapp'
urlpatterns = [
    
    path('', views.home_page, name='home_page'),
    path('face_shape_check/', views.face_shape_check, name='face_shape_check'),
    path('hair_style_suggestions/', views.hair_style_suggestions, name='hair_style_suggestions'),
    path('virtual_hairstyle/', views.VirtualHairstyleView.as_view(), name='virtual_hairstyle'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('appointment/', views.appointment, name='appointment'),
    path('appointment_manage/', views.appointment_manage, name='appointment_manage'),
]

