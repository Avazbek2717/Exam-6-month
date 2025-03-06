from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
# from apps.common.views import SponsorCreateAPIView, StudentSponsorCreateAPIView,StudentListAPIView, TotalAmountStatisticAPIView,MonthlyStatisticAPIView
from .schema import swagger_urlpatterns
from apps.common.views import NewsCreateView,SendEmail,BannerApiVeiw

urlpatterns = [
    path("admin/", admin.site.urls),
    path('send_news/',NewsCreateView.as_view()),
    path('send_email/',SendEmail.as_view()),
    path("banners/",BannerApiVeiw.as_view())
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
