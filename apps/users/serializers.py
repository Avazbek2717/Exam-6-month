<<<<<<< HEAD
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
=======
import random
import re
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from rest_framework import serializers
from .models import CustomUser  


class UserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=255, 
        required=True,
        write_only=True
    )
    password1 = serializers.CharField(
        max_length=255, 
        required=True, 
        write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, 
        required=True, 
        write_only=True
    )

    def validate(self, attrs):
        """Ma'lumotlarni tekshirish"""

        phone_number = attrs['phone_number']

        if not self.is_valid_phone(phone_number):
            raise serializers.ValidationError({"phone_number": "Telefon raqam noto‘g‘ri formatda!"})

        user = CustomUser.objects.filter(phone_number=phone_number, is_verified=True).first()
        
        if user:
            raise serializers.ValidationError({"phone_number": "Bu raqam bilan avval ro‘yxatdan o‘tilgan"})

        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password1": "Parollar mos kelmadi!"})

        if cache.get(phone_number):
            raise serializers.ValidationError({"phone_number": "2 daqiqadan keyin qayta urining"})
    
        return attrs

    @staticmethod
    def is_valid_phone(phone_number):
        """Telefon raqamni regex bilan tekshirish"""
        pattern = r"^\+998(33|55|77|88|90|91|93|94|95|97|98|99)\d{7}$"
        return re.match(pattern, phone_number) is not None
    

    def create(self, validated_data):
        """Foydalanuvchi yaratish"""
        phone_number = validated_data.pop("phone_number")
        password = validated_data.pop("password1")
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        
        if user:
            user.password = password
            user.save()
        else:
            user = CustomUser.objects.create_user(phone_number=phone_number)

        code = self.generate_random_number()
        cache.set(user.phone_number, code, timeout=120)
        print(f"Tasdiqlash kodi: {code}")  # Debug uchun

        return user

    @staticmethod
    def generate_random_number():
        """Tasdiqlash kodi yaratish"""
        return ''.join([str(random.randint(0, 9)) for _ in range(5)])


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)

    def validate(self, attrs):

        phone_number = attrs['phone_number']

        if not self.is_valid_phone(phone_number):
            raise serializers.ValidationError({"phone_number": "Telefon raqam noto‘g‘ri formatda!"})

        """Login ma'lumotlarini tekshirish"""
        user = CustomUser.objects.filter(phone_number=phone_number, is_verified=True).first()

        if not user:
            raise serializers.ValidationError({"phone_number": "Iltimos, avval ro'yhatdan o'ting!"})

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": "Parol noto‘g‘ri!"})
        
        return attrs

    @staticmethod
    def is_valid_phone(phone_number):
        """Telefon raqamni regex bilan tekshirish"""
        pattern = r"^\+998(33|55|77|88|90|91|93|94|95|97|98|99)\d{7}$"
        return re.match(pattern, phone_number) is not None


class ResendVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, required=True, write_only=True)

    def validate(self, attrs):

        phone_number = attrs['phone_number']
        user = CustomUser.objects.filter(phone_number=phone_number, is_verified=True)

        if not user:
            raise serializers.ValidationError({"phone_number": "Bu raqam bilan foydalanuvchi topilmadi yoki tasdiqlangan!"})
        
        if cache.get(phone_number):
            raise serializers.ValidationError({"phone_number": "Tasdiqlash kodini 2 daqiqadan keyin qayta so‘rang!"})

        return attrs

    def create(self, validated_data):
        phone_number = validated_data['phone_number']

        existing_code = cache.get(phone_number)

        if existing_code:
            code = existing_code
            message = "Avval yuborilgan tasdiqlash kodidan foydalaning"
            print(code)
        else:
            code = self.generate_random_number()
            cache.set(phone_number, code, timeout=120)
            message = 'Yangi tasdiqlash kodi yaratildi va yuborildi!'
            print(code)
        
        return {"message": message}
    
    @staticmethod
    def generate_random_number():
        """Tasdiqlash kodi yaratish"""
        return ''.join([str(random.randint(0, 9)) for _ in range(5)])


class SetNewPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, required=True, write_only=True)
    code = serializers.CharField(max_length=5, required=True, write_only=True)
    new_password1 = serializers.CharField(max_length=255, required=True, write_only=True)
    new_password2 = serializers.CharField(max_length=255, required=True, write_only=True)

    def validate(self, attrs):
        """Tasdiqlash kodini tekshirish va yangi parolni validatsiya qilish"""
        phone_number = attrs["phone_number"]
        code = attrs["code"]

        cached_code = cache.get(phone_number)
        if not cached_code or cached_code != code:
            raise serializers.ValidationError({"code": "Tasdiqlash kodi noto‘g‘ri yoki eskirgan!"})

        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password1": "Parollar mos kelmadi!"})

        return attrs

    def create(self, validated_data):
        """Yangi parolni saqlash"""
        phone_number = validated_data["phone_number"]
        new_password = validated_data["new_password1"]

        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if not user:
            raise serializers.ValidationError({"phone_number": "Bu raqam bilan foydalanuvchi topilmadi!"})

        user.set_password(new_password)
        user.save()
        cache.delete(phone_number)

        return {"message": "Parol muvaffaqiyatli o‘zgartirildi!"}


class ChangePasswordInsideSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5, required=False, write_only=True)
    old_password = serializers.CharField(max_length=255, required=True, write_only=True)
    new_password = serializers.CharField(max_length=255, required=True, write_only=True)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        cache_code = cache.get(f'change_{user.phone_number}')

        if attrs.get('code'):
            if not cache_code:
                raise serializers.ValidationError({"code": "Kod mavjud emas"})
            
            if attrs['code'] != str(cache_code):
                raise serializers.ValidationError({"code": "Kod xato kiritildi"})
        
        if not check_password(attrs['old_password'], user.password):
            raise serializers.ValidationError({"old_password": "Eski parol noto‘g‘ri!"})

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cache_key = f"change_{user.phone_number}"
        cache_code = cache.get(cache_key)

        if cache_code and not validated_data.get("code"):
            raise serializers.ValidationError({"code": "Siz allaqachon kod olgansiz, uni kiriting."})

        if validated_data.get("code"):
            user.set_password(validated_data.get("new_password"))
            user.save()
        else:
            code = self.generate_random_number()
            cache.set(cache_key, code, timeout=120)
            raise serializers.ValidationError({"code": "SMS kodni kiriting"})

        return validated_data
>>>>>>> cbf5bc9c972a4fa54b8c86e7d872a84e9ea20606
