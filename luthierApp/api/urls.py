from django.urls import path
from . import views

urlpatterns = [
    # api paths list
    path('', views.index, name='index'),
    # register
    path('register/', views.register, name='register'),
    # listings
    path('listings/', views.get_listings, name='listings'),
    path('listings/<str:pk>', views.get_listing, name='listing'),
    # luthiers
    path('luthiers/', views.get_luthiers, name='listing'),
    path('luthiers/<str:pk>', views.get_luthier, name='listing'),
    # dict entities
    path('categories/', views.get_categories, name='categories'),
    path('brands/', views.get_brands, name='brands'),
    path('statuses/', views.get_statuses, name='statuses'),
    path('payment_methods/', views.get_payment_methods,
         name='payment methods'),
]
