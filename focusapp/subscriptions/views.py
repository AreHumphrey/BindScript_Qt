
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SubscriptionSerializer, HwidCheckSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .serializers import SubscriptionUpdateSerializer
from .models import Subscription
from focusapp.users.models import CustomUser


class SubscriptionList(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class HwidCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = HwidCheckSerializer(data=request.data)
        if serializer.is_valid():
            hwid = serializer.validated_data['hwid']
            if hwid == request.user.hwid:
                return Response({"status": "allowed"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HwidResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.hwid = request.data.get('hwid', '')
        request.user.save()
        return Response({"status": "hwid reset successful"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_subscription(request):
    serializer = SubscriptionUpdateSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        subscription_type = serializer.validated_data['subscription_type']
        duration_days = serializer.validated_data['duration_days']

        try:
            user = CustomUser.objects.get(username=username)
            end_date = timezone.now() + timedelta(days=duration_days)
            subscription, created = Subscription.objects.get_or_create(
                user=user,
                defaults={'subscription_type': subscription_type, 'end_date': end_date}
            )
            if not created:
                subscription.subscription_type = subscription_type
                subscription.end_date = end_date
                subscription.save()

            user.subscription = subscription
            user.subscription_end = subscription.end_date
            user.save()

            return Response({'message': 'Subscription updated successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_expired_subscriptions(request):
    expired_subscriptions = Subscription.objects.filter(end_date__lt=timezone.now())
    for subscription in expired_subscriptions:
        user = subscription.user
        user.subscription = None
        user.subscription_end = None
        user.save()
        subscription.delete()
    return Response({'message': 'Expired subscriptions deleted successfully'}, status=status.HTTP_200_OK)
