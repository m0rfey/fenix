from .models import User
from .serializers import UserSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serialized_user = UserSerializer(users, many=True)
        return Response(serialized_user.data)

class UserDetail(APIView):

    def get_objsect(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_objsect(pk)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)
