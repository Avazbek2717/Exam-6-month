from rest_framework import serializers
from . import models
import random
from django.core.cache import cache


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=255,
        required=True,
        write_only = True,
    )
    password1 = serializers.CharField(
        max_length = 255,
        required = True, 
        write_only = True
    )
    password2 = serializers.CharField(
        max_length = 255, 
        required = True, 
        write_only = True
    )

    def validate(self, attrs):
        phone = attrs.get('phone')

        user = models.CustomUser.objects.filter(phone=phone, is_verified=True).first()

        if user:
            raise serializers.ValidationError({'phone': "This number has been registered before."})
        
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password1': "Passwords does not match"})
        
        print(cache.get(phone))
        
        if cache.get(phone):
            raise serializers.ValidationError({'phone': '2 daqiqadan so\'ng urinib ko\'ring'})
        
        return attrs
    
    def create(self, validated_data):
        user = models.CustomUser.objects.filter(phone=validated_data['phone']).first()

        if user:
            user.password = validated_data['password1']
        else:
            user = models.CustomUser.objects.create_user(
                phone=validated_data.pop('phone'), password=validated_data.pop('password1')
            )

        code = self.generate_random_number()
        cache.set(user.phone, code, timeout=120)
        print(code)
        return user
    
    
    '''Generate verification code'''
    @staticmethod
    def generate_random_number():
        return ''.join([str(random.randint(0, 9)) for _ in range(5)])