# goats_app/serializers.py
from rest_framework import serializers
from .models import User, Goat, Load, Sales

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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
