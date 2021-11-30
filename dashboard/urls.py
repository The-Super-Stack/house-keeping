from django.urls import path
from .views import main, employee as emp, supervisor as sv

app_name = 'dash'

urlpatterns = [
    path('', main.level_check, name='main'),
    path('is-invited-you/<slug:link>', main.invitation_registering, name='manual-registering'),
    path('Registered', main.LandingPage.as_view(), name='registered'),
    path('delete', sv.delete_all_assignment_control, name='delete-all'),
]

urlpatterns += [
    path('Supervisor', sv.DashboardView.as_view(), name='home'),
    path('Supervisor/show_qr/<qr_code>', sv.ShowQRCode.as_view(), name='qr-code'),
    path('Supervisor/LokasiKerja', sv.CreateWorkPlace.as_view(), name='create-work'),
    path('Supervisor/BerikanPekerjaan', sv.create_job, name='create-job'),
    path('generate_link', sv.CreateInvitationLink.as_view(), name='links'),
]

urlpatterns += [
    path('Employee', emp.EmployeeDashboard.as_view(), name='emp'),
    path('Employee/<int:pk>/', emp.qr_validating, name='emp-qr'),
    path('Employee/<int:pk>/list', emp.MyJobDetail.as_view(), name='emp-list'),
    path('Employee/<int:pk>/done', emp.set_list_to_done, name='emp-done'),
    path('Employee/<int:pk>', emp.UpdateJob.as_view(), name='emp-do'),
]

