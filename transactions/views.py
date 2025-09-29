
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny 
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework import generics
from .serializers import UserCreateSerializer
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer




class TransactionViewSet(viewsets.ModelViewSet):
    # Definiciones estándar de DRF
    queryset = Transaction.objects.all().order_by('-transaction_date')
    serializer_class = TransactionSerializer
    

    def get_permissions(self):
        """
        Define los permisos basados en el método HTTP:
        - GET (Listado de Admin) requiere un token JWT válido.
        - POST (Pasarela de Pago) es totalmente público.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()] 
        
        # POST, PUT, DELETE, etc., son públicos (Pasarela de Pago).
        # Esto previene el error 'CSRF token missing' en la pasarela.
        return [AllowAny()]
    



class UserRegisterView(generics.CreateAPIView):
    # Esta vista es solo para un uso temporal y único.
    serializer_class = UserCreateSerializer
    permission_classes = [] # Permitir acceso público TEMPORALMENTE


