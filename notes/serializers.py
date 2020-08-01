from rest_framework import serializers
from .models import (
    CustomUser,
    Note
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ['user']


class NoteViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["note"]
