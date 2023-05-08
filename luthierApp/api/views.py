from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import *

@api_view((['GET']))
def index(request):
    routes = [
        # listings
        '/api/listings',
        '/api/listings/<id>/',
        '/api/listings/create',
        '/api/listings/delete/<id>/',
        # orders
        '/api/products/<update>/<id>/',

    ]
    return Response(routes)

@api_view(['GET'])
def get_listings(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_listing(request, pk):
    listing = Listing.objects.get(id=pk)
    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)


############### dict entity views

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_statuses(request):
    statuses = Status.objects.all()
    serializer = StatusSerializer(statuses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_payment_methods(request):
    payment_methods = PaymentMethod.objects.all()
    serializer = PaymentMethodSerializer(payment_methods, many=True)
    return Response(serializer.data)
