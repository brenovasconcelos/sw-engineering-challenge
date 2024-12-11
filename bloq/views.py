from rest_framework import viewsets
from .models import Bloq
from .serializers import BloqSerializer

# Create your views here.

class BloqViewSet(viewsets.ModelViewSet):
    queryset = Bloq.objects.all()
    serializer_class = BloqSerializer
