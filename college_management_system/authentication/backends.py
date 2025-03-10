from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailBackend(ModelBackend):
    """
    Custom authentication backend to allow users to login with their email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the provided username is actually an email
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
        return None