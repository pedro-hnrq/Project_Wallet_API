from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from accounts.models import User


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Gera o token JWT com informações adicionais.
        """
        token = super().get_token(user)
        token['user_id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)

        return {
            "access_token": data.pop('access'),
            "refresh_token": data.pop('refresh'),
            "type": "Bearer",
            "expiration_at": token["exp"],
            "issued_at": token["iat"],
            "jti": token["jti"],
            "user": {
                'id': self.user.id,
                'email': self.user.email
            },
        }


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=12
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def validate_password(self, value):
        if len(value) < 8 or len(value) > 12:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        return value

    def create(self, validated_data):
        # O método create_user já lida com a criptografia da senha
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return {'access_token': data['access']}


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        try:
            super().validate(attrs)
            return {'message': 'Token Válido'}
        except Exception as e:
            return {'message': 'Token Inválido', 'error': str(e)}
