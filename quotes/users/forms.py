"""Forms(limits) for user models in quotesapp"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """A form for user registration.

    This form extends the built-in UserCreationForm to include fields for
    creating a new user account. It provides validation for username and
    passwords and ensures that the passwords match.

    Args:
        UserCreationForm (Form): Django's built-in form for user registration.
    """
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput()
    )
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput()
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput()
    )

    class Meta:
        """Meta class for specifying model and fields."""
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    """A form for user login.

    This form extends the built-in AuthenticationForm to provide fields for
    user authentication. It validates the username and password against
    the database.

    Args:
        AuthenticationForm (Form): Django's built-in form for user authentication.
    """

    class Meta:
        """Meta class for specifying model and fields."""
        model = User
        fields = ['username', 'password']
