from django.urls import path
from .views import employee as emp, main, supervisor as spv

app_name = 'api'

""" main Urls """
urlpatterns = [
    path('', main.documentation, name='main'),
    path('login', main.UserLogin.as_view(), name='login-api'),
    path('user', main.UserAuthenticated.as_view(), name='user-auth'),
    path('logout', main.UserLogout.as_view(), name='logout'),
]

""" this is the part for the employee side """
urlpatterns += [
    path('assignment-control', emp.assignment_control, name='emp-ass'),
    path('assignment-control/img/<slug:uid>', emp.img_upload, name='emp-ass'),
    path('assignment-control/list/<slug:uid>', emp.assignment_list_detail, name='emp-ass'),
    path('qr-validating/<slug:uid>', emp.qr_validating, name='emp-det'),
]

""" this is the part of the supervisor """
urlpatterns += [
    path('supervisor', spv.AssignmentListOnMine.as_view(), name='spv'),
    path('supervisor/all-employee', spv.all_employee, name='all_emp'),
    path('supervisor/work-place', spv.WorkPlaceEndPoint.as_view(), name='work-place'),
    path('supervisor/links', spv.CreateInvitationLinkAPI.as_view(), name='links'),
]
