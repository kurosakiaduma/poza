from booking.models import Persona

class EmailAuthBackend():
    def authenticate(self, request, username, password):
        try:
            user = Persona.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except Persona.DoesNotExist:
            pass
        return None

    def get_user(self, uuid):
        try:
            return Persona.objects.get(pk=uuid)
        except:
            return None
        