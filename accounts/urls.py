from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name="accounts"
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="userlogout"),
    path('signup/', views.UserRegistrationView.as_view(), name="signup"),
    path('users/', views.UsersListView.as_view(), name="userList"),
    path('users/search/', views.UserSearchView.as_view(), name="userSearch"),
]
