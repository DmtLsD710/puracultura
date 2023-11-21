# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

# Definimos una nueva clase de backend de autenticación que hereda de ModelBackend
class EmailOrUsernameBackend(ModelBackend):
    # Redefinimos el método authenticate
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Obtenemos el modelo de usuario
        UserModel = get_user_model()
        # Buscamos usuarios que tengan el nombre de usuario o el correo electrónico proporcionado
        users = UserModel.objects.filter(
            Q(username=username) | Q(email=username)
        )
        # Iteramos sobre los usuarios encontrados
        for user in users:
            # Si el usuario tiene la contraseña proporcionada y puede autenticarse, lo devolvemos
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        # Si no encontramos ningún usuario, devolvemos None
        return None
