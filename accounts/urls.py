from django.urls import path
from .views import UserLogin, UserLogout, UserRegister

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', UserRegister.as_view(), name='register'),
]
