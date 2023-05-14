import datetime
from rest_framework import permissions
import jwt
from jwt.exceptions import DecodeError
from django.core.exceptions import ObjectDoesNotExist

from .models import User

SYMMETRICAL_KEY = 'SYMMETRICAL_KEY'

def valdidate_user_exist_in_db_and_token_expiry(request):
    token = request.COOKIES.get('jwt')
    unix_time_now = int(datetime.datetime.utcnow().timestamp())
    if not token:
        return {}
    try:
        payload = jwt.decode(token.encode('utf-8'), SYMMETRICAL_KEY, algorithms=['HS256'])
        if unix_time_now > payload['expiration']:
            return {}
        User.objects.get(id=payload['id'])
        return payload
    except (ObjectDoesNotExist, DecodeError):
        return {}

class IsUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        payload = valdidate_user_exist_in_db_and_token_expiry(request)  
        return True if payload else False

class IsLuthierPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        payload = valdidate_user_exist_in_db_and_token_expiry(request)
        if payload:
            if payload['user_type'] == 2:
                return True
            return False