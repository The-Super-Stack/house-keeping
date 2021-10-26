# from .main import *
#
#
# class CreateWorkPlace(CreateView):
#     model = WorkPlace
#     template_name = 'd/form.html'
#     form_class = CreateWorkPlaceForm
#
#     def get_success_url(self):
#         return reverse('dash:home')
#
#     def form_valid(self, form):
#         form.instance.qr_code = generate_code()
#         return super(CreateWorkPlace, self).form_valid(form)
#
#     def dispatch(self, request, *args, **kwargs):
#         return super(CreateWorkPlace, self).dispatch(request, *args, **kwargs)
#
#
# class DashboardView(ListView):
#     template_name = 'd/home.html'
#     model = WorkPlace
#     context_object_name = 'jobs'
#
#     def get_context_data(self, **kwargs):
#         context = super(DashboardView, self).get_context_data(**kwargs)
#         employee = self.request.user.employeemanagement.is_employee
#         supervisor = self.request.user.employeemanagement.is_supervisor
#         if employee and supervisor:
#             stat = 'supervisor'
#         else:
#             stat = 'employee'
#         context['stat'] = stat
#         return context
#
#
# def create_job(request):
#     emp = EmployeeManagement.objects.filter(is_employee=True, is_supervisor=False)
#     form = CreateEmployeeJob()
#
#     if request.method == 'POST':
#         form = CreateEmployeeJob(request.POST or None, request.FILES or None)
#         emp_list = request.POST.get('emp')
#         if form.is_valid():
#             for employee in emp_list:
#                 form.instance.user = employee
#                 form.save()
#
#     context = {
#         'employee': emp,
#         'form': form,
#     }
#     return render(request, '', context)
