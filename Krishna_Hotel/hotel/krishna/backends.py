from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel

# from django.contrib.auth.models import User
from .models import Account
from django.core.exceptions import ValidationError


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field = "{}__iexact".format(
                UserModel.USERNAME_FIELD
            )
            user = UserModel._default_manager.get(
                **{case_insensitive_username_field: username}
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = Account.objects.get(username=username)
        if user is not None:
            group = user.groups.all().first().name
            print("User's group is: ", group)
            print("Username: ", username)
            print("Inputed Password: ", password)
            print("Actual Password: ", user.password)
            print("User is super: ", user.is_superuser)
            if user.password == password:
                print("Password correct")
                return user
            else:
                print("Password incorrect")
                return None
        else:
            print("Invalid credentials you dummy!")
            raise ValidationError("Invalid credentials you dummy!")

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
