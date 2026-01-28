from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode

@csrf_exempt
@api_view(["POST"])
def user_register(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

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
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "user": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    return Response({"error": "Invalid credentials"}, status=400)


#  3. FORGOT PASSWORD
token_generator = PasswordResetTokenGenerator()
@csrf_exempt
@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")

    if not User.objects.filter(email=email).exists():
        return Response({"error": "Email not found"}, status=400)

    user = User.objects.get(email=email)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

    send_mail(
        "TaskBrisk Password Reset",
        f"Click the link to reset your password:\n{reset_link}",
        "yourgmail@gmail.com",
        [email],
        fail_silently=False,
    )

    return Response({"message": "Password reset email sent"})

#reset password

@csrf_exempt
@api_view(["POST"])
def reset_password(request):
    uid = request.data.get("uid")
    token = request.data.get("token")
    password = request.data.get("password")

    try:
        uid_decoded = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid_decoded)
    except:
        return Response({"error": "Invalid link"}, status=400)

    if not token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=400)

    user.set_password(password)
    user.save()

    return Response({"message": "Password reset successful!"})
