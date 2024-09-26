from knox.views import LogoutView, LogoutAllView
from django.urls import path
from user import views
from user.views import Login, LoginAPI, UserStatus, SaveFiles, ChangeTune

urlpatterns = [
    path("index/", views.index, name="index"),
    path("user/<int:pk>/", views.UserData.as_view(), name="user"),
    path('', Login.as_view(), name="login"),
    path('login/api/', LoginAPI.as_view(), name="login_api"),
    path('api/user/status/', UserStatus.as_view(), name="user_status"),
    path('api/files/', SaveFiles.as_view(), name="files"),
    path('api/tune/', ChangeTune.as_view(), name="files"),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/logout/all/', LogoutAllView.as_view(), name='logout_all'),
]
