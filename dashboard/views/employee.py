from .main import *


class EmployeeDashboard(ListView):
    model = AssignmentControl
    template_name = 'd/em.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return AssignmentControl.objects.filter(
            worker=self.request.user
        )

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        emp = self.request.user.emp_user.is_employee
        spv = self.request.user.emp_user.is_supervisor
        if emp and not spv:
            return super(EmployeeDashboard, self).dispatch(request, *args, **kwargs)
        elif emp and spv:
            return redirect('dash:home')
        logout(self.request)
        return redirect('/accounts/login/')


class UpdateJob(UpdateView):
    model = AssignmentControl
    query_pk_and_slug = True
    pk_url_kwarg = 'pk'
    template_name = 'd/form.html'

    def get_success_url(self):
        return reverse('dash:emp')

    def get_form_class(self):
        get_assignment = get_object_or_404(AssignmentControl, pk=self.kwargs['pk'])
        if get_assignment.on_progress:
            self.form_class = MarkAsDone
        else:
            self.form_class = SetOnProgress
        return self.form_class

    def form_valid(self, form):
        get_assignment = get_object_or_404(AssignmentControl, pk=self.kwargs['pk'])
        if get_assignment.on_progress:
            form.instance.is_done = True
            form.instance.on_progress = False
            form.instance.end_time = timezone.now()
        else:
            form.instance.on_progress = True
            form.instance.start_time = timezone.now()
        return super(UpdateJob, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        get_assignment = get_object_or_404(AssignmentControl, pk=self.kwargs['pk'])
        if get_assignment.is_done or not get_assignment.access_permission:
            return HttpResponseRedirect(reverse('dash:emp'))
        return super(UpdateJob, self).dispatch(request, *args, **kwargs)


def do_job(request, pk):
    get_assignment = get_object_or_404(AssignmentControl, pk=pk)
    if request.method == 'POST':
        if get_assignment.on_progress:
            get_assignment.end_time = timezone.now()
            get_assignment.is_done = True
            get_assignment.on_progress = False
            get_assignment.save()
        elif get_assignment.is_done:
            pass
        else:
            get_assignment.start_time = timezone.now()
            get_assignment.on_progress = True
            get_assignment.save()
    return redirect('dash:emp')


def qr_validating(request, pk):
    context = {}
    get_assignment = get_object_or_404(AssignmentControl, pk=pk)
    work = get_assignment.assignment.qr_code
    if request.method == 'POST':
        qr_code = request.POST.get('qr_c')
        if qr_code is not None and qr_code == work:
            get_assignment.access_permission = True
            get_assignment.save()
            return HttpResponseRedirect(reverse('dash:emp-do', args=[pk]))
    context['this_ass'] = work
    return render(request, 'd/read.html', context)
