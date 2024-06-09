from django.urls import path
from .views import SubscriptionList, SubscriptionDetail, HwidCheckView, HwidResetView

urlpatterns = [
    path('', SubscriptionList.as_view(), name='subscription-list'),
    path('<int:pk>/', SubscriptionDetail.as_view(), name='subscription-detail'),
    path('hwid-check/', HwidCheckView.as_view(), name='hwid-check'),
    path('hwid-reset/', HwidResetView.as_view(), name='hwid-reset'),
]
