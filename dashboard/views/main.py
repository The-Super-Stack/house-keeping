# from django.core.exceptions import ImproperlyConfigured
# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.generic import *
# from django.utils import timezone
# from ..forms import *
# from django.urls import reverse
# from django.http import HttpResponseRedirect, HttpResponse
# from ..utils import generate_code
#
#
# def level_check(request):
#     employee = request.user.employeemanagement.is_employee
#     supervisor = request.user.employeemanagement.is_supervisor
#     if employee and supervisor:
#         return redirect('dash:home')
#     elif employee:
#         return redirect('dash:emp')
#     else:
#         return render(request, 'd/home.html', {'stat': 'Mohon bersabar sampai akun mu diverifikasi'})
