from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.utils import timezone
from ..forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from ..utils import generate_code, spv_code_generator, assignment_code, invitation_code
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib import messages
import datetime, pytz


def level_check(request):
    link = request.GET.get('link')
    if link:
        linked = InvitationLink.objects.filter(link=link)
        if linked:
            return HttpResponseRedirect(reverse('dash:manual-registering', args=[link]))

    if request.user.is_authenticated:
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
    return redirect('/accounts/login/?next=/')


def register_manual(request):
    form = CreateMainUserForm()
    e_form = UserExtendedForm()
    if request.method == 'POST':
        # get supervisor code
        spv_code = request.POST.get('spv_code')
        if spv_code:
            get_spv = EmployeeManagement.objects.filter(code=spv_code)
            if get_spv:
                spv = get_object_or_404(EmployeeManagement, code=spv_code)
                if spv.is_employee and spv.is_supervisor:
                    form = CreateMainUserForm(request.POST or None, request.FILES or None)
                    e_form = UserExtendedForm(request.POST or None, request.FILES or None)
                    """ get data from form """
                    username = request.POST.get('username')
                    password1 = request.POST.get('password1')
                    password2 = request.POST.get('password2')
                    email = request.POST.get('email')
                    f_name = request.POST.get('first_name')
                    l_name = request.POST.get('last_name')
                    if password1 == password2:
                        if form.is_valid() and e_form.is_valid():
                            user = User.objects.create_user(username=username, password=password2)
                            user.email = email
                            user.first_name = f_name
                            user.last_name = l_name
                            # user.save()
                            e_form.instance.user = user
                            e_form.instance.supervisor = spv.user
                            emp_data = EmployeeManagement.objects.all()
                            code_data = [x.code for x in emp_data]
                            code = spv_code_generator()
                            while True:
                                if code in code_data:
                                    code = spv_code_generator()
                                else:
                                    break

                            e_form.instance.code = spv_code_generator()
                            # e_form.save()
                            return redirect('dash:registered')

    context = {
        'form': form,
        'e_form': e_form
    }
    return render(request, 'd/reg.html', context)


class LandingPage(TemplateView):
    template_name = ''


def invitation_registering(request, link):
    get_link = InvitationLink.objects.filter(link=link)
    e_form = UserExtendedForm()
    form = CreateMainUserForm()
    if not get_link:
        return redirect('')

    get_link = get_object_or_404(InvitationLink, link=link)
    link_time = get_link.valid_until
    nowadays = datetime.datetime.now()
    time_now = pytz.utc.localize(nowadays)
    opened = True
    if not time_now <= link_time:
        messages.warning(request, "Form Ini sudah tidak menerima respon")
        opened = False
    if request.method == 'POST':
        """ get supervisor code """
        the_spv = get_link.spv
        spv = get_object_or_404(EmployeeManagement, user=the_spv)
        if spv.is_employee and spv.is_supervisor:
            """ get data from form """
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            f_name = request.POST.get('first_name')
            l_name = request.POST.get('last_name')
            if password1 == password2:
                if form.is_valid() and e_form.is_valid():
                    user = User.objects.create_user(username=username, password=password2)
                    user.email = email
                    user.first_name = f_name
                    user.last_name = l_name
                    # user.save()
                    e_form.instance.user = user
                    e_form.instance.supervisor = spv.user
                    emp_data = EmployeeManagement.objects.all()
                    code_data = [x.code for x in emp_data]
                    code = spv_code_generator()
                    while True:
                        if code in code_data:
                            code = spv_code_generator()
                        else:
                            break

                    e_form.instance.code = code
                    # e_form.save()
                    return redirect('dash:registered')
            messages.warning(request, "Password yang kamu input tidaklah sama! Mohon Periksa ulang")

    context = {
        'form': form,
        'e_form': e_form,
        'open': opened
    }
    return render(request, 'd/reg.html', context)
