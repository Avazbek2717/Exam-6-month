from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .schema import swagger_urlpatterns
from apps.common.views import NewsCreateView,SendEmail,BannerApiVeiw,ProductDetailAPIView,ReviewAPIView,ContactUsAPIView,NewArrivalsApiView,TestimonalAPIView,OrderListCreateAPIView
from apps.common.views import OrderRetrieveUpdateDestroyAPIView,OrderItemListCreateAPIView,OrderItemRetrieveUpdateDestroyAPIView,send_notification_view,NotificationRetrieveUpdateDestroyAPIView,NotificationListCreateAPIView

from rest_framework.routers import DefaultRouter




urlpatterns = [
    path("admin/", admin.site.urls),
    path('send_news/',NewsCreateView.as_view()),
    path('send_email/',SendEmail.as_view()),
    path("banners/",BannerApiVeiw.as_view()),
    path('product_detail/<int:pk>/', ProductDetailAPIView.as_view()),
    path('product_review/',ReviewAPIView.as_view()),
    path('contact_us/',ContactUsAPIView.as_view()),
    path('new_arrivals_product/',NewArrivalsApiView.as_view()),
    path('testimonal/',TestimonalAPIView.as_view()),
    path('orders/', OrderListCreateAPIView.as_view()),   # GET, POST
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view()),  # GET, PUT, PATCH, DELETE
    path('order-items/', OrderItemListCreateAPIView.as_view()),  # GET, POST
    path('order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view()),
    path('send-notification/', send_notification_view, name='send_notification'),
    path('notifications/', NotificationListCreateAPIView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationRetrieveUpdateDestroyAPIView.as_view(), name='notification-detail'),
    path('users/',include("apps.users.urls"))

]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
