from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
import re

# def validate_phone(value):
#     phone_regex = re.compile(r'^\+998\d{9}$')
#     if not phone_regex.match(value):
#         raise ValidationError('Telefeon raqam xato formatda yuborildi')


'''Manager to create users by phone number'''
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
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }