from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from ..serializers import *
from django.db.models import Q as __
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status


@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def all_employee(request):
    emp = EmployeeManagement.objects.all()
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


@api_view(['GET'])
def assignment_control(request):
    wr = request.GET.get('wr')
    assignment = AssignmentControl.objects.all()
    assignment = assignment.filter(worker_id=wr)
    serializer = AssignmentSerializer(assignment, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'POST'])
def qr_validating(request, uid):
    try:
        assignment = get_object_or_404(AssignmentControl, uid=uid)
    except AssignmentControl.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssignmentSerializer(assignment, many=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        code = request.data['code']
        get_place = assignment.assignment.qr_code
        if code and code == get_place:
            assignment.access_permission = True
            assignment.save()
        serializer = AssignmentSerializer(assignment, many=False)
        return Response(serializer.data, status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def img_upload(request, uid):
    try:
        assignment = get_object_or_404(AssignmentControl, uid=uid)
    except AssignmentControl.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        serializer = AssignmentSerializer(assignment, many=False)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def assignment_list_detail(request, uid):
    try:
        get_ass = get_object_or_404(AssignmentControl, uid=uid)
        dataset = AssignmentListControl.objects.filter(assignment_control=get_ass)
    except AssignmentControl.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ListControlSerializer(dataset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pk = request.data['id']
        is_done = request.data['is_done']

        for index, num in enumerate(pk):
            done = is_done[index]
            get_assignment_list = get_object_or_404(AssignmentListControl, pk=num)
            if done:
                get_assignment_list.is_done = True
            else:
                get_assignment_list.is_done = False
            get_assignment_list.save()

        serializer = ListControlSerializer(dataset, many=True)
        return Response(serializer.data)

