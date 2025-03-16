from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
<<<<<<< HEAD
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
import re
=======
from django.core import validators
from django.utils.deconstruct import deconstructible
from rest_framework_simplejwt.tokens import RefreshToken

>>>>>>> cbf5bc9c972a4fa54b8c86e7d872a84e9ea20606

# def validate_phone(value):
#     phone_regex = re.compile(r'^\+998\d{9}$')
#     if not phone_regex.match(value):
#         raise ValidationError('Telefeon raqam xato formatda yuborildi')


<<<<<<< HEAD
'''Manager to create users by phone number'''
=======
>>>>>>> cbf5bc9c972a4fa54b8c86e7d872a84e9ea20606
class CustomUserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqam kiritilishi shart!")

        phone_regex = re.compile(r'^\+998\d{9}$')
        if not phone_regex.match(phone):
            raise ValidationError('Telefeon raqam xato formatda yuborildi')

        extra_fields.setdefault("is_active", True)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    "Create a superuser (admin)"
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

<<<<<<< HEAD
        return self.create_user(phone, password=None, **extra_fields)
    

class CustomUser(AbstractUser):
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()  
    
    username = None
    phone = models.CharField(
        max_length=20,
        unique=True,
        #validators=[validate_phone],
        verbose_name='Telefon raqam'
        )
    is_verified = models.BooleanField(default=False, verbose_name='Tasdiqlangan')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone)

    def tokens(self):
=======
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone_number, password, **extra_fields)

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


    username = None
    first_name = None  

    phone_validator = PhoneValidator()
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Phone number',
        validators=[phone_validator],
        unique=True
    )
    full_name = models.CharField(max_length=255, verbose_name='Full Name', blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Ushbu maydonni qo'shing

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.id} - {self.phone_number} - {self.full_name}"

    def tokens(self):
        """Foydalanuvchi uchun JWT tokenlarni yaratadi"""
>>>>>>> cbf5bc9c972a4fa54b8c86e7d872a84e9ea20606
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
<<<<<<< HEAD
        }
=======
        }
>>>>>>> cbf5bc9c972a4fa54b8c86e7d872a84e9ea20606
