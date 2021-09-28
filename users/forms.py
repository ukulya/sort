from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()


class AddNewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "phone", "email")
        field_classes = {'username': UsernameField}
