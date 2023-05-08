from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class LuthierProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = LuthierProfile
        fields = '__all__'

    def to_representation(self, instance):
        data = super(LuthierProfileSerializer, self).to_representation(instance)
        user = data.pop('user')
        for key, val in user.items():
            data.update({key: val})
        return data


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def to_representation(self, instance):
        data = super(CustomerProfileSerializer, self).to_representation(instance)
        user = data.pop('user')
        for key, val in user.items():
            data.update({key: val})
        return data


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

# dict entity serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'