from django.urls import path

from . import views

app_name = 'myapp'
urlpatterns = [
    
    path('', views.home_page, name='home_page'),
    path('face_shape_check/', views.face_shape_check, name='face_shape_check'),
    path('function/hair_style_suggestions/', views.hair_style_suggestions, name='hair_style_suggestions'),
    path('virtual_hairstyle/', views.virtual_hairstyle, name='virtual_hairstyle'),
    path('appointment/', views.appointment, name='appointment'),
    path('appointment_manage/', views.appointment_manage, name='appointment_manage'),

]