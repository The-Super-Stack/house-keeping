from .main import *
from django.db.models import Q as __
from django.contrib.auth.models import User


@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def all_employee(request):
    emp = EmployeeManagement.objects.exclude(is_supervisor=True)
    serializer = EmployeeSerializer(emp, many=True)

    if request.GET:
        nik = request.GET.get('nik')
        phone = request.GET.get('ph')
        if nik or phone:
            if nik:
                emp = emp.filter(__(nik__icontains=nik))
            elif phone:
                emp = emp.filter(phone_number=phone)
        elif phone and nik:
            emp = emp.filter(__(nik__icontains=nik), phone_number=phone)

        serializer = EmployeeSerializer(emp, many=True)
    return Response(serializer.data)


class AssignmentListOnMine(APIView):
    def get(self, format=None):
        me = self.request.GET.get('me')
        assignment = AssignmentControl.objects.filter(given_by=me)
        serializer = AssignmentSerializer(assignment, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        me = self.request.GET.get('me')
        date = self.request.data['date']
        est_time = self.request.data['time']
        assignment = self.request.data['assignment']
        emp_list = self.request.data['employee']

        for emp in emp_list:
            get_worker = get_object_or_404(EmployeeManagement, pk=int(emp))
            user = get_object_or_404(User, id=int(me))
            get_work_place = get_object_or_404(WorkPlace, id=assignment)
            job = AssignmentControl.objects.create(
                assignment=get_work_place, estimated_time=est_time,
                worker=get_worker.user, for_day=date,
                given_by=user, uid=assignment_code()
            )
            job.save()
            get_list = AssignmentList.objects.filter(for_job=int(assignment))
            for ass_list in get_list:
                list_control = AssignmentListControl.objects.create(
                    assignment_control=job,
                    assignment_list=ass_list
                )
                list_control.save()

        ass = AssignmentControl.objects.filter(given_by=me)
        serializer = AssignmentSerializer(ass, many=True)
        return Response(serializer.data, status.HTTP_201_CREATED)


class WorkPlaceEndPoint(APIView):
    def get(self, format=None):
        wp = WorkPlace.objects.all()
        serializer = WorkPlaceSerializer(wp, many=True)
        return Response(serializer.data)
