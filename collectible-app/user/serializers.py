from django.contrib.auth import authenticate, get_user_model as gum
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


# The serializer for users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = gum()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # Create a new user with encrypted password and return it
    def create(self, validated_data):
        return gum().objects.create_user(**validated_data)


# Serializer for the user authentication object
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # Validate and authenticate a user
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            error = _('These authentication credentials are not correct!')
            raise serializers.ValidationError(error, code='authentication')

        attrs['user'] = user
        return attrs
