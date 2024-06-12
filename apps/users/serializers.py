from rest_framework import serializers
from .models import User, OneTimePassword


class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'phone_number', 'email')

    def validate(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user= User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            username=validated_data.get('username'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number')
            )
        return user


class OneTimePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneTimePassword
        fields = ('user', 'otp')