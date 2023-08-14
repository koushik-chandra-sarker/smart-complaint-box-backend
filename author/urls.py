from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from author.views import MyTokenObtainPairView, ChangePasswordView, varify_mail_address, GetDesignationViewSet

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('change-password/', ChangePasswordView.as_view(), name='password_change'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('verify-mail/', varify_mail_address),
    path('get-designatoin/', GetDesignationViewSet.as_view({'get': 'list'}), name="get_designation"),


]
