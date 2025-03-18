from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from . import serializers
from rest_framework.views import APIView
from .models import CustomUser
from django.db.models import Count,Sum



class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({"data": user.tokens()}, status=201)


class CodeVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code_from_user = self.request.data.get("code", None)
        code = cache.get(user.phone_number, None)

        if not code_from_user:
            raise ValidationError({"code": "Kiritish shart"})

        if not code:
            raise ValidationError({"code": "Kod eskirgan"})

        if code_from_user != code:
            raise ValidationError({"code": "Kod xato kiritildi"})

        user.is_verified = True
        user.save()

        return Response('success')


class LoginAPIView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        phone = self.request.data.get("phone_number")

        user = CustomUser.objects.filter(phone_number=phone).first()

        return Response({"tokens": user.tokens()})
    

class ResendVerificationCodeView(APIView):

    def post(self,request):
        serializer = serializers.ResendVerificationCodeSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.save(),status=200)

        return Response(serializer.errors,status=400)


class SetNewPassword(APIView):

    def post(self, request):
        serializer = serializers.SetNewPasswordSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.save(), status=200)

        return Response(serializer.errors, status=400)
    

class ChangePasswordApi(generics.CreateAPIView):
    serializer_class = serializers.ChangePasswordInsideSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


