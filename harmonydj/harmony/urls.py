from django.urls import path
from . import views

app_name = 'harmony'

urlpatterns = [
    path('', views.home, name='home'),
    path('enquire/', views.enquire, name='enquire'),
    path('media/hero.png', views.hero_image, name='hero_image'),
    path('units/', views.units_list, name='units_list'),
    path('units/dashboard/', views.units_dashboard, name='units_dashboard'),
    path('units/<slug:slug>/', views.unit_detail, name='unit_detail'),
]
