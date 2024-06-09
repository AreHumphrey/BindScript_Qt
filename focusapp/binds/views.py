from rest_framework import viewsets
from .models import Bind
from .serializers import BindSerializer


class BindViewSet(viewsets.ModelViewSet):
    queryset = Bind.objects.all()
    serializer_class = BindSerializer
