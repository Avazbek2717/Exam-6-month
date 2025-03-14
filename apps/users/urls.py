from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserRegisterAPIView.as_view()),
    path('verify-code/', views.CodeVerificationAPIView.as_view()),
    path('reset-code/', views.ResendVerificationCodeView.as_view()),
    path("set-new-password/", views.SetNewPassword.as_view()),
    path("change-password/", views.ChangePasswordApi.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    
]
