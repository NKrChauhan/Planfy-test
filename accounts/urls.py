from .views import LogoutView,LoginView, RegisterView,UpdateUserView,UserDetailView,DeleteUserView,change_password
from django.urls import path ,include
app_name = 'account'

urlpatterns = [
    path('login/',LoginView,name="login"),
    path('register/',RegisterView,name="register"),
    path('logout/',LogoutView,name="logout"),
    path('me/',UserDetailView.as_view(),name="user_detail"),
    path('user/delete/',DeleteUserView.as_view(),name="user_delete"),
    path('update_me/',UpdateUserView.as_view(),name="user_update"),
    path('password/',change_password, name='change_password'),
]