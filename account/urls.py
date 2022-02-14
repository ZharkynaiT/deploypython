from django.urls import path
from account.views import RegistrationView, ActivationView, LogOutView, ForgotPasswordView, CompleteRestPasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/<str:email>/<str:code>/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('forgot_password/<str:email>/', ForgotPasswordView.as_view()),
    path('complete_recovery/', CompleteRestPasswordView.as_view()),

]