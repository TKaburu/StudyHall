from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('profile/<str:username>/', views.UserProfile.as_view(), name='profile'),
    path('profile/', views.UpdateUser.as_view(), name='update-user')
]