from rest_framework.serializers import ModelSerializer
from .models import BoardModel

class BoardSerializer(ModelSerializer):
    class Meta:
        model = BoardModel
        fields = ['id', 'user']
        read_only_fields = ['id', 'user']