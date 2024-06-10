from django.urls import path
from .views import CustomUserList, CustomUserDetail, RegisterView, LoginView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', CustomUserList.as_view(), name='customuser-list'),
    path('<int:pk>/', CustomUserDetail.as_view(), name='customuser-detail'),
]

