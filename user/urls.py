from django.urls import path
from guest import views
app_name="user"
urlpatterns = [
    path('Home/', views.home,name="login"),
    
]