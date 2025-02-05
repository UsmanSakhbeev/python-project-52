from django.contrib.auth.forms import UserCreationForm

from task_manager.users.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "second_name",
        ) + UserCreationForm.Meta.fields


class CustomUserChangeForm(CustomUserCreationForm):
    pass
