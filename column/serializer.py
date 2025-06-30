from rest_framework.serializers import ModelSerializer
from .models import ColumnModel

class ColumnSerializer(ModelSerializer):
    class Meta:
        model = ColumnModel
        fields = ["id", "board", "status"]

