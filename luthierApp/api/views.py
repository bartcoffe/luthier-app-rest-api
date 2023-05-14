import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
import jwt

from .models import *
from .serializers import *

SYMMETRICAL_KEY = 'SYMMETRICAL_KEY'
JWT_COOKIE_AUTH = 'JWT_COOKIE_AUTH'
SIMPLE_JWT_LOCAL_STORE = 'SIMPLE_JWT_LOCAL_STORE'

USER_AUTH = JWT_COOKIE_AUTH

@api_view((['POST']))
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

def jwt_cookie_response(user, expiration_min):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_min)
    payload = {
        'id': user.id,
        'expiration': int(expiration.timestamp()),
        'iat': int(datetime.datetime.utcnow().timestamp())
    }
    token = jwt.encode(payload, key=SYMMETRICAL_KEY, algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {'jwt': token}
    return response

@api_view((['POST']))
def login(request):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.get(email=email)
    if user is None:
        raise AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise AuthenticationFailed('incorrect password')
    if USER_AUTH == JWT_COOKIE_AUTH:
        return jwt_cookie_response(user=user, expiration_min=60)
    elif USER_AUTH == SIMPLE_JWT_LOCAL_STORE:
        return 'xd'

@api_view((['GET']))
def auth_user(request):
    if USER_AUTH == JWT_COOKIE_AUTH: 
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload = jwt.decode(token, SYMMETRICAL_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif USER_AUTH == SIMPLE_JWT_LOCAL_STORE:
        'xd'

@api_view((['GET']))
def logout(request):
    if USER_AUTH == JWT_COOKIE_AUTH:
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

@api_view((['GET']))
def index(request):
    routes = [
        # register
        '/api/register/',
        # listings
        '/api/listings',
        '/api/listings/<id>/',
        '/api/listings/create',
        '/api/listings/delete/<id>/',
        # orders
        '/api/products/<update>/<id>/',
        # dict tables
        '/api/categories/',
        '/api/brands/',
        '/api/statuses/',
        '/api/payment_methods/',

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


@api_view(['GET'])
def get_luthiers(request):
    luthier = LuthierProfile.objects.all()
    serializer = LuthierProfileSerializer(luthier, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_luthier(request, pk):
    luthier = LuthierProfile.objects.get(user_id=pk)
    serializer = LuthierProfileSerializer(luthier, many=False)
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
