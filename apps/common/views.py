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
from .permisson import *
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer


class NewsCreateView(APIView):
    permission_classes = [IsAdminUser]
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
    # permission_classes = [CanWriteReview]

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request,*args,**kwargs)
    #     return  Response({"message": "Send your review"})



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


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """ Buyurtmani yangilashda mahsulotlar va miqdorlar to‘g‘ri ekanligini tekshirish """
        order = self.get_object()
        new_items = self.request.data.get('items', [])
        total_price = 0
        validated_items = []

        for item in new_items:
            product = Product.objects.get(id=item['product'])
            quantity = item['quantity']

            if product.stock < quantity:
                raise serializers.ValidationError(f"{product.title} uchun yetarli zaxira mavjud emas.")

            total_price += product.price * quantity
            validated_items.append(item)

        serializer.context['order_items'] = validated_items
        serializer.save(total_price=total_price)


class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """ OrderItem yangilanishida mahsulot va miqdor mosligini tekshirish """
        order_item = self.get_object()
        product = serializer.validated_data.get('product', order_item.product)
        quantity = serializer.validated_data.get('quantity', order_item.quantity)

        if product.stock + order_item.quantity < quantity:
            raise serializers.ValidationError(f"{product.title} mahsuloti uchun yetarli ombor zaxirasi yo‘q.")
        
        # Oldingi zaxirani tiklash va yangi miqdorni kamaytirish
        product.stock += order_item.quantity
        product.stock -= quantity
        product.save()
        serializer.save()




from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class IsAdminUser(permissions.BasePermission):
    """
    Faqat admin foydalanuvchilar ruxsat olishi mumkin
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class NotificationCreateAPIView(generics.CreateAPIView):
    """Foydalanuvchi faqat yangi bildirishnoma yaratishi mumkin"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]  # Faqat adminlarga ruxsat

    def perform_create(self, serializer):
        """Bildirishnoma yaratilgandan keyin WebSocket orqali yuborish"""
        notification = serializer.save()
        notification.send_notification()


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    """Barcha bildirishnomalarni olish va yangi bildirishnoma yaratish"""
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Faqat adminlar

    def perform_create(self, serializer):
        """Bildirishnomani yaratish va WebSocket orqali yuborish"""
        notification = serializer.save()
        notification.send_notification()  # WebSocket orqali yuborish

class NotificationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Bitta bildirishnomani olish, yangilash yoki o‘chirish"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Faqat adminlar


class TopsSellerApiView(APIView):

    def get(self,request):
        limit = int(request.query_params.get('limit',4))

        top_seller = Product.objects.annotate(total_sold = Sum("orderitem__quantity")).order_by("-total_sold")[:limit]

        serializer = ProductSerializer(top_seller,many = True)

        return Response(serializer.data,status=200)
    

class ReviewListApiView(generics.ListAPIView):
    serializer_class = ReviewsListSerializer
    permission_classes = [IsAuthenticated]  # Faqat login qilganlar ko‘ra oladi

    def get_queryset(self):
        """ Foydalanuvchiga yozilgan sharhlarni qaytarish """
        return Review.objects.filter(user=self.request.user)
