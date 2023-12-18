from rest_framework import serializers
from .models import Medicine 
from Authentication.models import User


class timeListField(serializers.ListField):
    def to_representation(self, obj):
        return obj.split(',') if obj else []
    def to_internal_value(self, data):
        return ','.join(data) if data else ''


class MedicineSerializer(serializers.ModelSerializer):
    select_time = timeListField()
    class Meta: 
        model = Medicine
        fields = '__all__'
        read_only_fields = ('id', 'patient', 'create_time')

