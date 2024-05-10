from django.urls import path
from userauths import views
app_name = "userauths"
urlpatterns = [
    path('sign-up/',views.register_view,name='sign-up'),
    path('loginform/',views.user_login,name='loginform'),
      path('logout/', views.user_logout, name='logout'),
]

