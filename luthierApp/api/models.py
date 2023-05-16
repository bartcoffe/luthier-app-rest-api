from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save

CUSTOMER = 1
LUTHIER = 2
ADMIN = 3

USER_TYPE_CHOICES = (
      (CUSTOMER, 'customer'),
      (LUTHIER, 'luthier'),
      (ADMIN, 'admin'),
  )

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', ADMIN)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=True, db_index=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
class LuthierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name="luthier_profile")
    about = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name="customer_profile")
    nickname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    customer = models.ForeignKey(CustomerProfile,
                                 on_delete=models.SET_NULL,
                                 null=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    instrument_brand = models.ForeignKey(Brand,
                                         on_delete=models.SET_NULL,
                                         null=True)
    year_produced = models.IntegerField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ListingPictureUrl(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=False)
    url = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.url


class ProfilePictureUrl(models.Model):
    profile = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=False)
    url = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.url


class Status(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name_plural = "statuses"

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    number = models.IntegerField(null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    postal_code = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name_plural = "shipping addresses"

    def __str__(self):
        return f'{self.street} {self.number} {self.city}'


class Order(models.Model):
    luthier = models.ForeignKey(LuthierProfile,
                                on_delete=models.SET_NULL,
                                null=True)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    current_status = models.ForeignKey(Status,
                                       on_delete=models.SET_NULL,
                                       null=True)
    payment_method = models.ForeignKey(PaymentMethod,
                                       on_delete=models.SET_NULL,
                                       null=True)
    service_description = models.TextField(null=False, blank=False)
    service_price = models.DecimalField(max_digits=6,
                                        decimal_places=2,
                                        null=True,
                                        blank=True)
    shipping_price = models.DecimalField(max_digits=6,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
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

def create_user_profile(sender, **kwargs):
    user_instance = kwargs['instance']
    created = kwargs['created']
    user_type = getattr(user_instance, 'user_type')

    if user_type == CUSTOMER:
        if created:
            CustomerProfile.objects.create(user=user_instance)
    if user_type == LUTHIER:
        if created:
            LuthierProfile.objects.create(user=user_instance)

def hide_listing_when_order_is_taken(sender, **kwargs):
    """
    when a luthier takes a job (clicks on a listing effectively making a POST request to create an order for a given lisitng)
    the new Order entry is created and the listing is being updated so that it's not visible to other luthiers. 
    """
    order_instance = kwargs['instance']
    created = kwargs['created']
    if created:
        listing = getattr(order_instance, 'listing')
        listing.is_visible = False
        listing.save()


post_save.connect(create_order_status_entry, sender=Order)
post_save.connect(create_user_profile, sender=User)
post_save.connect(hide_listing_when_order_is_taken, sender=Order)
