from django.urls import path

from user import views
from user.views import Login, LoginAPI

urlpatterns = [
    path("index/", views.index, name="index"),
    path("user/<int:pk>/", views.UserData.as_view(), name="user"),
    path('', Login.as_view(), name="login"),
    path('login/api/', LoginAPI.as_view(), name="login_api"),

]
