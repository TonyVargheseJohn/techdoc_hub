
from django.urls import path
from guest import views
app_name="guest"
urlpatterns = [
    path('Login/', views.login,name="login"),
    path('user_registration/',views.user_registration,name="user_registration"),
    path('Home/', views.home,name="Home"),
    
]