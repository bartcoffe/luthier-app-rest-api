from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'user_type',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class LuthierProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = LuthierProfile
        fields = '__all__'

    def to_representation(self, instance):
        unwanted_user_info = ['user_type']
        data = super(LuthierProfileSerializer, self).to_representation(instance)
        user = data.pop('user')
        for key, val in user.items():
            if key not in unwanted_user_info:
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
