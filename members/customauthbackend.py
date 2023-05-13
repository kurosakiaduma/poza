from booking.models import Patient

class EmailAuthBackend():
    def authenticate(self, request, username, password):
        try:
            user = Patient.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except Patient.DoesNotExist:
            pass
        return None

    def get_user(self, uuid):
        try:
            return Patient.objects.get(pk=uuid)
        except:
            return None
        