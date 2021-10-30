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


def register_manual(request):
    form = CreateMainUserForm()
    e_form = UserExtendedForm()
    if request.method == 'POST':
        # get supervisor code
        spv_code = request.POST.get('spv_code')
        if spv_code:
            get_spv = EmployeeManagement.objects.filter()
            # if spv_code:
        form = CreateMainUserForm(request.POST or None, request.FILES or None)
        e_form = UserExtendedForm(request.POST or None, request.FILES or None)
        # get data from form
        username = form.cleaned_data['username']
        password = request.POST.get('password')
        email = form.cleaned_data['email']
        f_name = form.cleaned_data['first_name']
        l_name = form.cleaned_data['last_name']
        if form.is_valid() and e_form.is_valid():
            user = User.objects.create_user()
            user.username = username
            user.password = password
            user.email = email
            user.first_name = f_name
            user.last_name = l_name
            user.save()
            e_form.instance.user = user

    context = {
        'form': form,
        'e_form': e_form
    }
    return render(request, 'd/reg.html', context)
