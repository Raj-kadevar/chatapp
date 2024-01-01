from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from knox.views import LoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserList, AuthSerializer

@login_required
def index(request):
    return render(request, "index.html",{"users":User.objects.filter(is_staff=False)})


class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, *args, **kwargs):
        return Response(template_name="login.html")


class UserData(RetrieveAPIView):
    serializer_class = UserList
    queryset = User.objects.filter(is_staff=False)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        messages = [
            {
                'profile':instance.profile.url,
                'name':instance.username,
            },
            {
                'message': 'hii '+instance.username,
                'sender': True,
            },
            {
                'message': 'hello ',
                'sender': False,
            }
        ]
        return Response(messages)

class LoginAPI(LoginView):
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
