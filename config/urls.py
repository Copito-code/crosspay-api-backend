"""
URL configuration for config project.
...
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions.views import TransactionViewSet
from transactions.views import UserRegisterView # Asegurar que esta importación exista
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_http_methods 


# Importaciones de JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# -------------------------------------------------------------
# 💥 SOLUCIÓN CORS EXTREMA (Solo para Preflight OPTIONS)
# -------------------------------------------------------------
# Esta función intercepta la petición OPTIONS para /api/token/ y envía los headers CORS.

@csrf_exempt 
@require_http_methods(["OPTIONS"])
def options_view(request, *args, **kwargs):
    # Esto garantiza que el navegador reciba la respuesta necesaria para pasar el CORS
    response = HttpResponse()
    # Forzamos los encabezados que el navegador espera para tu origen local
    response['Access-Control-Allow-Origin'] = 'http://localhost:5173' 
    response['Access-Control-Allow-Methods'] = 'POST, OPTIONS' # El login usa POST
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Max-Age'] = '86400' 
    response.status_code = 200
    return response

# -------------------------------------------------------------
# FIN SOLUCIÓN CORS EXTREMA
# -------------------------------------------------------------


# 1. Configurar el Router para la API
router = DefaultRouter()
# Esto crea rutas como /api/transactions/ (GET/POST)
router.register(r'transactions', TransactionViewSet) 

urlpatterns = [
    path('admin/', admin.site.urls), 
    
    # Asumo que esta ruta de registro existe en tu proyecto completo
    path('api/register/', UserRegisterView.as_view(), name='register'), 

    # 💥 CRUCIAL: Añadimos la función de OPTIONS justo antes del endpoint de POST
    path('api/token/', options_view, name='token_options_preflight'), 

    # ENDPOINTS DE JWT: Obtiene el 'access' y 'refresh' token (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    
    # Renueva el token (sesiones largas)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    
    # Exponemos la API (transactions)
    path('api/', include(router.urls)), 
]