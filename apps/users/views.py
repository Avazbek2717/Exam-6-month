from rest_framework import generics
from rest_framework.exceptions import ValidationError
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.cache import cache


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            'data': user.tokens()
        }, status=201)
    

class CodeVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code_from_user = self.request.data.get('code', None)
        code = cache.get(user.phone, None)

        if not code_from_user:
            raise ValidationError({'code': 'Kiritish shart'})
        
        if not code:
            raise ValidationError({'code': 'Kod eskirgan'})
        
        if code_from_user != code:
            raise ValidationError({'code': 'Kod xato kiritildi'})
        
        user.is_verified = True
        user.save()

        return Response('success')