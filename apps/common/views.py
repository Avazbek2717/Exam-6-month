
from rest_framework.generics import CreateAPIView, ListAPIView
from . import models
from rest_framework.views import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import News
from .serializers import NewsCreateSerializer
from core.task import send_newsletter
from rest_framework import generics
from .models import *
from .serializers import *

class NewsCreateView(APIView):
    """ Admin yangilik qo‘shsa, avtomatik obunachilarga jo‘natiladi """


    def post(self, request):
        serializer = NewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.save()  # Yangilikni saqlaymiz
            
            # Celery taskni chaqiramiz
            send_newsletter.delay(news.id)

            return Response(
                {"message": "News created and sent to subscribers!", "news": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SendEmail(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SendEmailSerializer