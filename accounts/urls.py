from .views import LogoutView,LoginView, RegisterView
from django.urls import path
app_name = 'accounts'

urlpatterns = [
    path('login/',LoginView,name="login"),
    path('register/',RegisterView,name="register"),
    path('logout/',LogoutView,name="logout"),
]