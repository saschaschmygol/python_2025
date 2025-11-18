from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MessageOut

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class TicketCloseSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(min_value=1)


class TicketAssignSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(min_value=1)


class TicketMessagesSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(min_value=1)


class OperatorReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageOut
        fields = ("text", "ticket_id")
