# serializers.py

from rest_framework import serializers
from .models import Report
from django.contrib.auth import get_user_model

User = get_user_model()



class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'post', 'report_type', 'details']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        # 不显示reporter字段
        report = Report.objects.create(**validated_data, reporter=self.context['request'].user)
        return report
    


class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'post', 'report_type', 'details', 'created_at', 'resolution_details', 'resolved_at', 'report_status']
        read_only_fields = ['id', 'post', 'report_type', 'details', 'created_at', 'resolution_details', 'resolved_at', 'report_status']

    

class AdminReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['id', 'post', 'report_type', 'details', 'created_at', 'reporter']






class ReportUpdateSerializer(serializers.ModelSerializer):
    report_status = serializers.ChoiceField(choices=Report.REPORT_STATUS, required=True)
    resolution_details = serializers.CharField(required=True)

    class Meta:
        model = Report
        fields = ['resolution_details', 'resolved_at', 'report_status']
        read_only_fields = ['resolved_at']

        



