from django.urls import path
from wadmin import views
app_name="wadmin"
urlpatterns = [
    path('Home/', views.home,name="Home"),
    
]