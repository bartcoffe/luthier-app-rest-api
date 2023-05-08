from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listings/', views.get_listings, name='listings'),
    path('brands/', views.get_brands, name='brands'),
]