from rest_framework import serializers
from dashboard.models import EmployeeManagement, AssignmentControl, AssignmentListControl, WorkPlace, AssignmentList, User


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


class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentList
        fields = '__all__'


class WorkPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlace
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
