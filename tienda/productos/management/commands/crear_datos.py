from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from productos.models import Producto
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea usuarios de prueba, grupos y productos de ejemplo'

    def handle(self, *args, **kwargs):
        # --- Crear usuarios ---
        superusuario, created = User.objects.get_or_create(
            username='superusuario',
            defaults={'email': 'super@correo.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            superusuario.set_password('admin123')
            superusuario.save()
            self.stdout.write(self.style.SUCCESS('Superusuario creado'))

        admin_test, created = User.objects.get_or_create(
            username='admin_test',
            defaults={'email': 'admin@test.com', 'is_staff': True}
        )
        if created:
            admin_test.set_password('admin123')
            admin_test.save()
            self.stdout.write(self.style.SUCCESS('Usuario admin_test creado'))

        user_normal, created = User.objects.get_or_create(
            username='user_normal',
            defaults={'email': 'user@test.com'}
        )
        if created:
            user_normal.set_password('user123')
            user_normal.save()
            self.stdout.write(self.style.SUCCESS('Usuario user_normal creado'))

        # --- Crear grupos ---
        grupo_admin, _ = Group.objects.get_or_create(name='Administradores')
        grupo_gestor, _ = Group.objects.get_or_create(name='Gestores de Productos')

        # --- Asignar permisos ---
        ct = ContentType.objects.get_for_model(Producto)
        permisos = Permission.objects.filter(content_type=ct)

        # Administradores: todos los permisos
        grupo_admin.permissions.set(permisos)

        # Gestores: solo add y change
        permisos_gestor = permisos.filter(codename__in=['add_producto', 'change_producto'])
        grupo_gestor.permissions.set(permisos_gestor)

        # --- Asignar usuarios a grupos ---
        admin_test.groups.add(grupo_admin)
        user_normal.groups.add(grupo_gestor)

        # --- Crear productos de ejemplo ---
        if not Producto.objects.filter(nombre='Producto 1').exists():
            Producto.objects.create(nombre='Producto 1', descripcion='Producto de prueba 1', precio=100.00, stock=10)

        if not Producto.objects.filter(nombre='Producto 2').exists():
            Producto.objects.create(nombre='Producto 2', descripcion='Producto de prueba 2', precio=200.00, stock=5)

        self.stdout.write(self.style.SUCCESS('Productos de ejemplo creados'))

        self.stdout.write(self.style.SUCCESS('¡Datos de prueba creados correctamente!'))
