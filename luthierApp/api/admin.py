from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Listing)
admin.site.register(ListingPictureUrl)
admin.site.register(Status)
admin.site.register(PaymentMethod)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderStatusHistory)