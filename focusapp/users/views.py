from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import CustomUser, Session
from .serializers import UserSerializer, SessionSerializer, CustomUserSerializer, UserCreateSerializer, \
    ChangePasswordSerializer, LoginSerializer

APPROVED_IPS = ['127.0.0.1']


class CustomUserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        print(f"Attempting login with username: {username} and password: {password}")

        # Проверка существования пользователя
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            print(f"User {username} does not exist")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка пароля
        if not user.check_password(password):
            print(f"Password for user {username} is incorrect")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({"error": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


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
