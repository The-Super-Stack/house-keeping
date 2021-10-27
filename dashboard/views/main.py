from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.utils import timezone
from ..forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from ..utils import generate_code
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout


@login_required(login_url='/accounts/login/')
def level_check(request):
    extended = EmployeeManagement.objects.filter(user=request.user)
    if extended.exists():
        employee = request.user.emp_user.is_employee
        supervisor = request.user.emp_user.is_supervisor
        if employee and supervisor:
            return redirect('dash:home')
        elif employee:
            return redirect('dash:emp')
        else:
            return render(request, 'd/home.html', {'stat': 'Mohon bersabar sampai akun mu diverifikasi'})

    logout(request)
    return redirect('/accounts/login/')
