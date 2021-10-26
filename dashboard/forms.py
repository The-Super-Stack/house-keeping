from django import forms
from .models import *


class SetOnProgress(forms.ModelForm):
    class Meta:
        model = AssignmentControl
        fields = ['img_before']


class MarkAsDone(forms.ModelForm):
    class Meta:
        model = AssignmentControl
        fields = ['img_after']


class CreateWorkPlaceForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = ['buildings', 'tower_name', 'ground_name', 'job_area']


class CreateEmployeeJob(forms.ModelForm):
    class Meta:
        model = AssignmentControl
        fields = ['assignment', 'estimated_time']
