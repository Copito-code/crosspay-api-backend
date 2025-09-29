# transactions/management/commands/createsuperuser_prod.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Crea un superusuario de forma no interactiva para el entorno de producción.'

    def handle(self, *args, **options):
        # ⚠️ CREDENCIALES FINALES
        # Usa estas credenciales para iniciar sesión en /admin/
        USERNAME = os.environ.get('SUPERUSER_NAME', 'admin770')
        EMAIL = os.environ.get('SUPERUSER_EMAIL', 'admin@gmail.com')
        PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
        
        User = get_user_model()
        
        if not User.objects.filter(username=USERNAME).exists():
            self.stdout.write(f'Creando superusuario {USERNAME}...')
            
            # 1. Crear el objeto usuario sin la contraseña
            user = User.objects.create(
                username=USERNAME,
                email=EMAIL,
            )
            
            # 2. Asignar la contraseña explícitamente y hashearla
            user.set_password(PASSWORD) 
            
            # 3. Asignar permisos de superusuario
            user.is_staff = True
            user.is_superuser = True
            
            # 4. Guardar los cambios
            user.save() 

            self.stdout.write(self.style.SUCCESS(f'Superusuario {USERNAME} creado exitosamente.'))
        else:
            self.stdout.write(f'El superusuario {USERNAME} ya existe. Saltando creación.')