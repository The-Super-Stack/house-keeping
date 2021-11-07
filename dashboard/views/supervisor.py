from .main import *
import time


class CreateWorkPlace(CreateView):
    model = WorkPlace
    template_name = 'd/form.html'
    form_class = CreateWorkPlaceForm

    def get_success_url(self):
        return reverse('dash:home')

    def form_valid(self, form):
        form.instance.qr_code = generate_code()
        return super(CreateWorkPlace, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateWorkPlace, self).dispatch(request, *args, **kwargs)


class DashboardView(ListView):
    template_name = 'd/home.html'
    model = AssignmentControl
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        employee = self.request.user.emp_user.is_employee
        supervisor = self.request.user.emp_user.is_supervisor
        if employee and supervisor:
            stat = 'supervisor'
        else:
            stat = 'employee'
        context['stat'] = stat
        return context

    def get_queryset(self):
        return AssignmentControl.objects.filter(given_by=self.request.user)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        spv = self.request.user.emp_user.is_supervisor
        emp = self.request.user.emp_user.is_employee
        if spv and emp:
            return super(DashboardView, self).dispatch(request, *args, **kwargs)
        elif emp and not spv:
            return redirect('dash:emp')
        logout(self.request)
        return redirect('/accounts/login/')


@login_required(login_url='/accounts/login/')
def create_job(request):
    emp = EmployeeManagement.objects.filter(is_employee=True, is_supervisor=False)
    form = CreateEmployeeJob()

    if request.method == 'POST':
        form = CreateEmployeeJob(request.POST or None, request.FILES or None)
        emp_list = request.POST.getlist('emp')
        print(emp_list)
        if form.is_valid():
            est_time = form.cleaned_data['estimated_time']
            assignment = form.cleaned_data['assignment']
            day = form.cleaned_data['for_day']
            for employee in emp_list:
                get_worker = get_object_or_404(EmployeeManagement, pk=int(employee))
                job = AssignmentControl.objects.create(
                    assignment=assignment, estimated_time=est_time,
                    worker=get_worker.user, for_day=day,
                    given_by=request.user, assignment_unique_id=assignment_code()
                )
                job.save()
                get_list = AssignmentList.objects.filter(for_job=assignment)
                for ass_list in get_list:
                    list_control = AssignmentListControl.objects.create(
                        assignment_control=job,
                        assignment_list=ass_list
                    )
                    list_control.save()
            return redirect('dash:home')
    context = {
        'employee': emp,
        'form': form,
    }
    return render(request, 'd/form.html', context)


def delete_all_assignment_control(request):
    dataset = AssignmentControl.objects.all()
    dataset_list = AssignmentListControl.objects.all()
    if request.method == 'POST':
        for data in dataset:
            data.delete()
        for lst in dataset_list:
            lst.delete()
    return redirect('dash:home')
