from django.urls import path
from .views import Admin, Register, Login, Logout, Info, DeleteUser
from publiceyeusa.settings import env

urlpatterns = [
    path("", Info.as_view(), name="info"),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("delete_user/", DeleteUser.as_view(), name="delete_user"),
    path(f"{env.get('REGISTER_ADMIN')}/", Admin.as_view(), name="register_admin")
]