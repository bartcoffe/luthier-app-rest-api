from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Category(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    class Meta:
        verbose_name_plural = "categories"
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    instrument_brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    year_produced = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class ListingPictureUrl(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=False)
    url = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.url

    
class Status(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    class Meta:
        verbose_name_plural = "statuses"
    def __str__(self):
        return self.name
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    number = models.IntegerField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    postal_code = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name_plural = "shipping addresses"

    
    def __str__(self):
        return f'{self.street} {self.number} {self.city}'
    
class Order(models.Model):
    luthier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    current_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    service_description = models.TextField(null=False, blank=False)
    service_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    shipping_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True)
    delivered_at = models.DateTimeField(null=True)
    def __str__(self):
        return str(f'{self.listing}')
    
class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "order status history"
    def __str__(self):
        return str(f'{self.order} | {self.status}')
    

def create_order_status_entry(sender, **kwargs):
    order_instance = kwargs['instance']
    new_status = getattr(order_instance, 'current_status')
    OrderStatusHistory.objects.create(order=order_instance, status=new_status)

post_save.connect(create_order_status_entry, sender=Order)
    