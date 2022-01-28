from django.contrib.auth import authenticate, get_user_model as gum
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _ # Put this to translate


# Serializes User data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = gum()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # Creates a new User with encrypted password and returns it
    def create(self, validated_data):
        return gum().objects.create_user(**validated_data)

    # Updates a User and sets the password properly
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


# Serializes the authentication token of a User
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    # Validates and authenticates a user
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            error = _('These authentication credentials are not correct!')
            raise serializers.ValidationError(error, code='authentication')

        attrs['user'] = user
        return attrs
