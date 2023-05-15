from django.urls import path
from . import views

urlpatterns = [
    # register, login
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.currently_logged_user, name='authenticated user'),
    # luthiers
    path('luthiers/', views.luthiers, name='luthiers'),
    path('luthiers/<str:pk>', views.luthier, name='luthier'),
    #customers
    path('customers/<str:pk>', views.customer, name='customer'),
    # listings
    path('listings/', views.listings, name='listings'),
    path('listings/<str:pk>', views.listing, name='listing'),
    # orders
    path('orders/', views.orders, name='orders'),
    path('orders/listing/<str:listing>', views.order_for_listing, name='order_for_listing'),
    # dict entities
    path('categories/', views.get_categories, name='categories'),
    path('brands/', views.get_brands, name='brands'),
    path('statuses/', views.get_statuses, name='statuses'),
    path('payment_methods/', views.get_payment_methods,
         name='payment methods'),
]
