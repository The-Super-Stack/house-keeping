from django.contrib.admin import site
from .models import *

site.register(EmployeeManagement)
site.register(AssignmentControl)
site.register(WorkPlace)
site.register(WorkingStatus)
site.register(AssignmentList)
site.register(AssignmentListControl)
