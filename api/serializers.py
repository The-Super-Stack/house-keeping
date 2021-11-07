from rest_framework import serializers
from dashboard.models import EmployeeManagement, AssignmentControl, AssignmentListControl, WorkPlace


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeManagement
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentControl
        fields = '__all__'


class ListControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentListControl
        fields = '__all__'
