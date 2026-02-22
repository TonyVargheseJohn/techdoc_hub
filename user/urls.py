from django.urls import path
from user import views
app_name="webuser"
urlpatterns = [
    path('Home/',views.home,name="home"),
    path('Myprofile/', views.myprofile,name="myprofile"),
    path('Editprofile/', views.editprofile,name="editprofile"),
    path('Viewannouncement/', views.viewannouncement,name="viewannouncement"),
    path('Viewmachine/', views.viewmachine,name="viewmachine"),
    path('uploadmachinefile/', views.upload_machine_file,name="upload_machine_file"),

   

    
]