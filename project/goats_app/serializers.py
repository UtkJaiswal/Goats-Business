# goats_app/serializers.py
from rest_framework import serializers
from .models import User, Goat, Load, Sales

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    name=validated_data['name'],
                    type=validated_data['type'],
                    )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goat
        fields = '__all__'

class LoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
