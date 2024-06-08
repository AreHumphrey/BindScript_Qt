from rest_framework import viewsets
from .models import CustomUser, Session
from .serializers import UserSerializer, SessionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

APPROVED_IPS = ['127.0.0.1']  # Массив одобренных IP-адресов


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


@api_view(['POST'])
def check_hwid(request):
    user = CustomUser.objects.get(username=request.data['username'])
    hwid = request.data['hwid']
    client_ip = request.META['REMOTE_ADDR']

    if client_ip not in APPROVED_IPS:
        return Response({"error": "IP address not approved"}, status=status.HTTP_403_FORBIDDEN)

    if user.hwid == hwid:
        return Response({"status": "approved"})
    else:
        return Response({"status": "denied"})


@api_view(['POST'])
def reset_hwid(request):
    user = CustomUser.objects.get(username=request.data['username'])
    user.hwid = request.data['new_hwid']
    user.save()
    return Response({"status": "hwid reset successful"})
