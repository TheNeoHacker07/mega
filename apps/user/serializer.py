from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="USER ALREADY EXISTS"
            )
        ]
    )

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "password", "password_confirm"]

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("PASSWORDS DIDNT MATCH")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("user not found")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("invalid email or password")

        attrs["user"] = user
        return attrs