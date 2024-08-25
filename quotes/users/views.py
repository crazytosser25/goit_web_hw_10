"""Views for users in quotesapp"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm


def signupuser(request):
    """Handles user registration.

    This view renders a registration form for new users. If the request is POST
    and the form is valid, it creates a new user and redirects to the main page.
    If the user is already authenticated, they are redirected to the main page.

    Args:
        request (HttpRequest): The HTTP request object containing data from
            the user.

    Returns:
        HttpResponse: The rendered template with the registration form or
            redirection to the main page.
    """
    if request.user.is_authenticated:
        return redirect(to='quotesapp:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})

def loginuser(request):
    """Handles user login.

    This view renders a login form for users. If the request is POST, it attempts
    to authenticate the user with the provided credentials. If authentication
    fails, an error message is displayed, and the user is redirected back to
    the login page. If the user is already authenticated, they are redirected
    to the main page.

    Args:
        request (HttpRequest): The HTTP request object containing login data.

    Returns:
        HttpResponse: The rendered template with the login form, an error
            message, or redirection to the main page.
    """
    if request.user.is_authenticated:
        return redirect(to='quotesapp:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quotesapp:main')

    return render(request, 'users/login.html', context={"form": LoginForm()})

@login_required
def logoutuser(request):
    """Handles user logout.

    This view logs out the currently authenticated user and redirects them
    to the main page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirection to the main page after logout.
    """
    logout(request)
    return redirect(to='quotesapp:main')
