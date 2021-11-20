from .main import *


@api_view(['GET'])
def assignment_control(request):
    wr = request.GET.get('wr')
    assignment = AssignmentControl.objects.all()
    assignment = assignment.filter(worker_id=wr)
    serializer = AssignmentSerializer(assignment, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def qr_validating(request, uid):
    try:
        assignment = get_object_or_404(AssignmentControl, uid=uid)
    except AssignmentControl.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssignmentSerializer(assignment, many=False)
        if not assignment.access_permission:
            return Response(status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data)

    elif request.method == 'POST':
        code = request.data['code']
        get_place = assignment.assignment.qr_code
        if code and code == get_place:
            assignment.access_permission = True
            assignment.save()
        serializer = AssignmentSerializer(assignment, many=False)
        return Response(serializer.data, status.HTTP_201_CREATED)

    # elif request.method == 'PUT':
    #     serializer = AssignmentSerializer(assignment, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


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
