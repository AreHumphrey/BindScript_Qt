
from django.urls import path
from .views import SubscriptionList, SubscriptionDetail, HwidCheckView, HwidResetView, update_subscription, delete_expired_subscriptions

urlpatterns = [
    path('', SubscriptionList.as_view(), name='subscription-list'),
    path('<int:pk>/', SubscriptionDetail.as_view(), name='subscription-detail'),
    path('hwid-check/', HwidCheckView.as_view(), name='hwid-check'),
    path('hwid-reset/', HwidResetView.as_view(), name='hwid-reset'),
    path('api/update_subscription/', update_subscription, name='update_subscription'),
    path('api/delete_expired_subscriptions/', delete_expired_subscriptions, name='delete_expired_subscriptions'),
]
