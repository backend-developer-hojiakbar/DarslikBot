from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, OneTimePassword
from rest_framework.decorators import action
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from .utils import send_generated_otp_to_email


class VerifyUserEmail(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        passcode = serializer.validated_data['otp']
        try:
            user_pass_obj = OneTimePassword.objects.get(otp=passcode)
            user = user_pass_obj.user

            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message': 'Account email verified successfully'
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'message': 'Passcode is invalid or user is already verified'
                }, status=status.HTTP_400_BAD_REQUEST)  # Batafsilroq xato xabari

        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'Passcode not provided'
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            send_generated_otp_to_email(user_data['email'], request)
            return Response({
                'data':user_data,
                'message':'thanks for signing up a passcode has be sent to verify your email'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = self.get_queryset()  # Retrieve all user records
        serializer = self.serializer_class(users, many=True)  # Serialize all user records
        return Response(serializer.data, status=status.HTTP_200_OK)


class OneTimePasswordViewSet(viewsets.ModelViewSet):
    queryset = OneTimePassword.objects.all()
    serializer_class = OneTimePasswordSerializer