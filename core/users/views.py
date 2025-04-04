from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from pydantic import ValidationError
from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect

def signup_view(request: Any) -> HttpResponse:
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                return render(request, 'errors.html', {'error': "Username already exists"})
            
            if User.objects.filter(email=email).exists():
                return render(request, 'errors.html', {'error': "Email already exists"})

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            response = HttpResponse("No content.")
            response["HX-Redirect"] = "/"
            return response

        except ValidationError as e:
            return render(request, 'errors.html', {'error': e.errors()})

    return render(request, "signup.html")

def login_view(request: Any) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponse("No content.")
            response["HX-Redirect"] = "/"
            return response

        return render(request, 'errors.html', {'error': "Invalid credentials"})

    return render(request, "login.html")

def logout_view(request: Any) -> HttpResponse:
    logout(request)
    return redirect("login")
