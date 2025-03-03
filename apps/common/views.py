from .serializers import SponsorCreateSerializer, StudentSponsorCreateSerializer,StudentListSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from . import models
from rest_framework.views import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.db.models import Sum


