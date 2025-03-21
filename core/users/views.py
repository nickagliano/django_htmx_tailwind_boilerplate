from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from pydantic import ValidationError
from typing import Any
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# FIXME: Redirect when user is already logged in
# FIXME: Add password_reset logic
# FIXME: Add OAuth?
def signup_view(request: Any) -> JsonResponse:
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                return render(request, 'users/errors.html', {'error': "Username already exists"})
            
            if User.objects.filter(email=email).exists():
                return render(request, 'users/errors.html', {'error': "Email already exists"})

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            response = HttpResponse("No content.")
            response["HX-Redirect"] = "/"  # FIXME: Can I add a flash here? -- Signup successful!
            return response

        except ValidationError as e:
            return render(request, 'users/errors.html', {'error': e.errors()})

    return render(request, "users/signup.html")

# FIXME: Add password_reset logic
# FIXME: Add OAuth?
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponse("No content.")
            response["HX-Redirect"] = "/"  # FIXME: Can I add a flash here?
            return response

        return render(request, 'users/errors.html', {'error': "Invalid credentials"})

    return render(request, "users/login.html")

# FIXME: Add OAuth?
def logout_view(request):
    logout(request)
    return redirect("login")
