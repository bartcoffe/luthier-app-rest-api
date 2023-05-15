import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
import jwt


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
        raise AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise AuthenticationFailed('incorrect password')
    return jwt_cookie_response(user=user, expiration_min=60)

@api_view((['GET']))
def currently_logged_user(request):
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
@permission_classes([IsLuthierPermission])
def listings(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsLuthierPermission | AccessSelfUserDataOnlyPermission])
def listing(request, pk):
    listing = Listing.objects.get(id=pk)
    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)

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