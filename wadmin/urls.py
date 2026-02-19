from django.urls import path
from wadmin import views
app_name="wadmin"
urlpatterns = [
    path('Home/', views.home,name="Home"),

    path('Myprofile/', views.myprofile,name="myprofile"),

    path('Addcategory/', views.addcategory,name="addcategory"),
    path('Editcategory/<int:eid>', views.editcategory,name="editcategory"),
    path('Deletecategory/<int:did>', views.deletecategory,name="deletecategory"),

    path('Machine/', views.machine, name="machine"),
    path('Editmachine/<int:eid>', views.editmachine, name="editmachine"),
    path('Deletemachine/<int:did>', views.deletemachine, name="deletemachine"),

    path('Announcement/', views.announcement, name="announcement"),
    path('Editannouncement/<int:eid>', views.editannouncement, name="editannouncement"),
    path('Deleteannouncement/<int:eid>', views.deleteannouncement, name="deleteannouncement"),


]