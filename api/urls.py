from django.urls import path
from .views import employee as emp

app_name = 'api'

""" this is the part for the employee side """
urlpatterns = [
    path('all-employee', emp.all_employee, name='all_emp'),
    path('assignment-control', emp.assignment_control, name='emp-ass'),
    path('assignment-control/img/<slug:uid>', emp.img_upload, name='emp-ass'),
    path('assignment-control/list/<slug:uid>', emp.assignment_list_detail, name='emp-ass'),
    path('qr-validating/<slug:uid>', emp.qr_validating, name='emp-det'),
]

""" this is the part of the """
