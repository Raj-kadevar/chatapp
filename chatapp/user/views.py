from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render
from knox.views import LoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from sentry_sdk.integrations.django import is_authenticated

from user.models import User, Chat, ChatGroup
from user.serializers import UserList, AuthSerializer, ChatMessageSerializer
from user.utils import group_name, check_status


@login_required
def index(request):
    return render(request, "index.html",{"users":User.objects.all().exclude(id=request.user.id)})


class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, *args, **kwargs):
        return Response(template_name="login.html")


class UserData(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserList
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        profile = [
            {
                'profile':instance.profile.url,
                'name':instance.username,
            },]
        grp_name = (
            Chat.objects.filter(group__name=group_name(request.user.id, self.kwargs['pk']))
        )
        serializer = ChatMessageSerializer(grp_name, many=True)
        return Response({"messages":serializer.data, "profile":profile})

class LoginAPI(LoginView):
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.status = True
        user.save()
        login(request, user)
        check_status(request.user.id,request.user.status)
        return super().post(request, format=None)


class UserStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.GET.get('status') == 'true':
            request.user.status = True
        else:
            request.user.status = False
        request.user.save()
        users = User.objects.all()
        serialized_users = serializers.serialize('json', users)
        check_status(request.user.id,request.user.status)
        return Response({"users":serialized_users})


class SaveFiles(APIView):

    def post(self, request, *args, **kwargs):
        grp_name = (
            ChatGroup.objects.get(name=group_name(int(request.data['receiver']), request.user.id))
        )
        files = request.FILES.getlist('files')
        for file in files:
            Chat.objects.create(group=grp_name, sender= request.user, images=file)
        return Response({"document_len":len(files),"user":request.user.id})


class ChangeTune(APIView):

    def get(self, request, *args, **kwargs):
        request.user.tune = 'audio/'+request.GET['audio']
        request.user.save()
        return Response({"status":"successful"})
