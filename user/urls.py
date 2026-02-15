from django.urls import path
from guest import views
app_name="webweuser"
urlpatterns = [
    path('Home/', views.home,name="home"),
    
]