from django.urls import path
from wadmin import views
from .views import admin_pie_report, admin_bar_report


app_name="wadmin"
urlpatterns = [
    path('Home/', views.home,name="Home"),

    path('Myprofile/', views.myprofile,name="myprofile"),
    path("Editprofile/", views.editprofile, name="editprofile"),
    path('changepassword/', views.changepassword, name='changepassword'),

    path('Addcategory/', views.addcategory,name="addcategory"),
    path('Editcategory/<int:eid>', views.editcategory,name="editcategory"),
    path('Deletecategory/<int:did>', views.deletecategory,name="deletecategory"),

    path('Machine/', views.machine, name="machine"),
    path('Editmachine/<int:eid>', views.editmachine, name="editmachine"),
    path('Deletemachine/<int:did>', views.deletemachine, name="deletemachine"),

    path('Announcement/', views.announcement, name="announcement"),
    path('Editannouncement/<int:eid>', views.editannouncement, name="editannouncement"),
    path('Deleteannouncement/<int:did>', views.deleteannouncement, name="deleteannouncement"),

    path('NewUsers/', views.newusers, name="newusers"),
    path('AcceptUser/<int:id>', views.acceptuser, name="acceptuser"),
    path('RejectUser/<int:id>', views.rejectuser, name="rejectuser"),
    path('AcceptedUsers/', views.acceptedusers, name="acceptedusers"),
    path('RejectedUsers/', views.rejectedusers, name="rejectedusers"),

    path("uploads/", views.view_uploaded_files, name="view_uploaded_files"),
    path("delete-upload/<int:id>/", views.delete_uploaded_file, name="delete_uploaded_file"),

    path('admin/report/', admin_pie_report, name='admin_pie_report'),
    path('admin/bar-report/', admin_bar_report, name='admin_bar_report'),




    # path('chat/', views.admin_chat_list, name='admin_chat_list'),
    # path('chat/<int:user_id>/', views.admin_chat, name='admin_chat'),
    # path('ajax/get-messages/', views.get_messages_admin, name='get_messages_admin'),
    # path('ajax/send-message/', views.send_message, name='send_message'),
    # path('ajax/mark-read/', views.mark_messages_read, name='mark_messages_read'),
    # path('ajax/total-unread/', views.total_unread_count, name='total_unread_count'),
    # path('ajax/delete-message/', views.delete_message, name='delete_message'),


# ── Chat pages ──
path('chat/',               views.admin_chat_list,    name='admin_chat_list'),
path('chat/<int:user_id>/', views.admin_chat,         name='admin_chat'),

# ── Chat AJAX ──
path('ajax/get-messages/',   views.get_messages_admin, name='get_messages_admin'),
path('ajax/send-message/',   views.send_message,       name='send_message'),
path('ajax/mark-read/',      views.mark_messages_read, name='mark_messages_read'),
path('ajax/delete-message/', views.delete_message,     name='delete_message'),
path('ajax/total-unread/',   views.total_unread_count, name='total_unread_count'),
]