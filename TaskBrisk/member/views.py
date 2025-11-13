from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(["POST"])
def user_register(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

    print("Incoming:", request.data)  # Debugging line

    if not email:
        return Response({"error": "Email is required"}, status=400)

    if password != confirm_password:
        return Response({"error": "Passwords do not match"}, status=400)

    # Check if user exists
    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        first_name=name,
        password=password
    )

    return Response({"message": "User registered successfully!"}, status=201)


#  2. LOGIN API
@csrf_exempt
@api_view(['POST'])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(username=email, password=password)

    if user:
        return Response({"message": "Login successful", "user": user.username})
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


#  3. FORGOT PASSWORD
@csrf_exempt
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get("email")

    if not User.objects.filter(username=email).exists():
        return Response({"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Normally you send OTP or reset link – for now return a message
    return Response({"message": "Password reset link sent to email"})