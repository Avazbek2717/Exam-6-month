
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
from rest_framework import generics,permissions
from .models import *
from .serializers import *

class NewsCreateView(APIView):
    """ Admin yangilik qo‘shsa, avtomatik obunachilarga jo‘natiladi """


    def post(self, request):
        serializer = NewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.save() 
            

            send_newsletter.delay(news.id)

            return Response(
                {"message": "News created and sent to subscribers!", "news": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SendEmail(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SendEmailSerializer


class BannerApiVeiw(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ReviewAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request,*args,**kwargs)
        return  Response({"message": "Send your review"})



class ContactUsAPIView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Message sent. We’ll contact you soon."}, status=status.HTTP_201_CREATED)
    

class NewArrivalsApiView(generics.ListAPIView):
    queryset = Product.objects.order_by('-created_at')
    serializer_class = NewArrivalsSerializer


class TestimonalAPIView(generics.ListAPIView):
    queryset = Testimonial.objects.all().order_by("-created_at")
    serializer_class = TestimonalSerializer







class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order_items = self.request.data.get('items', [])  
        validated_items = []

        total_price = 0
        for item in order_items:
            product = Product.objects.get(id=item['product'])
            quantity = item['quantity']
            
            if product.stock < quantity:
                raise serializers.ValidationError(f"{product.title} uchun yetarli zaxira mavjud emas.")
            
            total_price += product.price * quantity
            validated_items.append(item)

        serializer.context['order_items'] = validated_items
        serializer.save(total_price=total_price)

class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if product.stock < quantity:
            raise serializers.ValidationError(f"{product.title} mahsuloti uchun yetarli ombor zaxirasi yo‘q.")

        product.stock -= quantity 
        product.save()
        serializer.save()

class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
