from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


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
        fields = ['assignment', 'estimated_time', 'for_day']

        widgets = {
            'for_day': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'})
        }


class CreateMainUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserExtendedForm(forms.ModelForm):
    class Meta:
        model = EmployeeManagement
        fields = ['nik', 'profile_img', 'phone_number', 'gender']
