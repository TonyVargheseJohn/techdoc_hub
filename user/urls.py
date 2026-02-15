from django.urls import path
from user import views
app_name="webuser"
urlpatterns = [
    path('Home/',views.home,name="home"),
    path('Myprofile/', views.myprofile,name="myprofile"),
    path('Editprofile/', views.editprofile,name="editprofile"),

    
]