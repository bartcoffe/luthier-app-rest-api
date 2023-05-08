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
def get_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_listing(request, pk):
    listing = Listing.objects.get(_id=pk)
    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)