from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer, HwidCheckSerializer
from django.conf import settings

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
            # Проверка HWID пользователя
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
