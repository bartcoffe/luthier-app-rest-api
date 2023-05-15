import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
import jwt
from rest_framework import status

from .models import *
from .serializers import *
from .permissions import *

SYMMETRICAL_KEY = 'SYMMETRICAL_KEY'


@api_view((['POST']))
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view((['POST']))
def login(request):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.get(email=email)
    if user is None:
        raise PermissionDenied('user not found')
    if not user.check_password(password):
        raise PermissionDenied('incorrect password')
    return jwt_cookie_response(user=user, expiration_min=60)

@api_view((['GET']))
def currently_logged_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise PermissionDenied('unauthenticated')
    try:
        payload = jwt.decode(token, SYMMETRICAL_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise PermissionDenied('unauthenticated')
    user = User.objects.get(id=payload['id'])
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view((['GET']))
@permission_classes([IsUserPermission])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response


@api_view(['GET'])
def luthiers(request):
    luthier = LuthierProfile.objects.all()
    serializer = LuthierProfileSerializer(luthier, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([AccessSelfUserDataOnlyPermission])
def luthier(request, pk):
    luthier = LuthierProfile.objects.get(user_id=pk)
    if request.method == 'GET':
        serializer = LuthierProfileSerializer(luthier, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LuthierProfileSerializer(luthier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([AccessSelfUserDataOnlyPermission])
def customer(request, pk):
    customer = CustomerProfile.objects.get(user_id=pk)
    if request.method == 'GET':
        serializer = CustomerProfileSerializer(customer, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomerProfileSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
@api_view(['GET', 'POST'])
@permission_classes([IsUserPermission])
def listings(request):
    token = request.COOKIES.get('jwt')
    payload = jwt.decode(token.encode('utf-8'), SYMMETRICAL_KEY, algorithms=['HS256'])
    user_type = payload['user_type']
    if request.method == 'GET':
        if user_type == 1:       
            listings = Listing.objects.filter(customer = payload['id'])
        elif user_type == 2:
            listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if user_type == 1:
            request.data['customer'] = payload['id']
            serializer = ListingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied


@api_view(['GET'])
@permission_classes([IsLuthierPermission | AccessSelfUserDataOnlyPermission])
def listing(request, pk):
    listing = Listing.objects.get(id=pk)
    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsLuthierPermission])
def orders(request):
    token = request.COOKIES.get('jwt')
    payload = jwt.decode(token.encode('utf-8'), SYMMETRICAL_KEY, algorithms=['HS256'])
    if request.method == 'GET':    
        orders = Order.objects.filter(luthier = payload['id'])
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        request.data['luthier'] = payload['id']
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET'])
@permission_classes([IsUserPermission])
def order_for_listing(request, listing):
    order = Order.objects.get(listing=listing)
    serializer = OrderSerializer(order, many=False)
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


def jwt_cookie_response(user, expiration_min):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_min)
    payload = {
        'id': user.id,
        'user_type': user.user_type,
        'expiration': int(expiration.timestamp()),
        'iat': int(datetime.datetime.utcnow().timestamp())
    }
    token = jwt.encode(payload, key=SYMMETRICAL_KEY, algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {'jwt': token}
    return response