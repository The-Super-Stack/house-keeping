from django.urls import path
from .views import main, employee as emp, supervisor as sv

app_name = 'dash'

urlpatterns = [
    path('', main.level_check, name='main'),
    path('Register', main.register_manual, name='manual-registering')
]

urlpatterns += [
    path('Supervisor', sv.DashboardView.as_view(), name='home'),
    path('Supervisor/LokasiKerja', sv.CreateWorkPlace.as_view(), name='create-work'),
    path('Supervisor/BerikanPekerjaan', sv.create_job, name='create-job'),
]

urlpatterns += [
    path('Employee', emp.EmployeeDashboard.as_view(), name='emp'),
    path('Employee/<int:pk>/', emp.qr_validating, name='emp-qr'),
    path('Employee/<int:pk>/list', emp.MyJobDetail.as_view(), name='emp-list'),
    path('Employee/<int:pk>/done', emp.set_list_to_done, name='emp-done'),
    path('Employee/<int:pk>', emp.UpdateJob.as_view(), name='emp-do'),
]

