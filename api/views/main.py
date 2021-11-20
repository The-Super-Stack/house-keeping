from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from ..serializers import *
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status
from rest_framework.views import APIView
from dashboard.utils import assignment_code
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


def documentation(request):
    return render(request, 'api/doc.html')


class UserLogin(APIView):
    def get(self, format=None):
        return Response(status.HTTP_204_NO_CONTENT)

    def post(self, format=None):
        nik = self.request.data['nik']
        password = self.request.data['password']

        emp = EmployeeManagement.objects.filter(nik=nik)
        if not emp:
            raise AuthenticationFailed('User Not Found')

        emp = get_object_or_404(EmployeeManagement, nik=nik)
        user = emp.user
        auth = User.objects.filter(username=user.username).first()
        if not auth.check_password(password):
            raise AuthenticationFailed('Password is incorrect')

        payload = {
            'user_id': auth.id,
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'jwt': token
        }

        return response


class UserAuthenticated(APIView):
    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserLogout(APIView):
    def post(self, format=None):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'messages': 'Success',
            'status': status.HTTP_204_NO_CONTENT
        }
        return response
