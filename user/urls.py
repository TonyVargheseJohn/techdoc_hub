from django.urls import path
from user import views
app_name="webuser"
urlpatterns = [
    path('Home/',views.home,name="home"),

    path('Myprofile/', views.myprofile,name="myprofile"),
    path('Editprofile/', views.editprofile,name="editprofile"),
    path("changepassword/", views.changepassword, name="changepassword"),

    path('Viewannouncement/', views.viewannouncement,name="viewannouncement"),
    path("new-announcement-count/", views.new_announcement_count, name="new_announcement_count"),
    # user/urls.py
path("new-announcement-count/", views.new_announcement_count, name="new_announcement_count"),


    path("notifications/", views.my_notifications, name="notifications"),
    
    path('Viewmachine/', views.viewmachine,name="viewmachine"),
    path('uploadmachinefile/', views.upload_machine_file,name="upload_machine_file"),
    path("delete-upload/<int:id>/", views.delete_upload, name="delete_upload"),
    path('download-file/<int:fid>/', views.download_file, name='download_file'),
    path("myuploads/", views.my_uploads, name="my_uploads"),
    
    
    path("search-uploads/", views.search_uploads, name="search_uploads"),



    path("chat/<int:uid>/", views.chat_page, name="chat"),
    path("send-message/", views.send_message, name="send_message"),
    path("fetch-messages/<int:uid>/", views.fetch_messages, name="fetch_messages"),
    path("chat-users/", views.chat_users, name="chat_users"),
    path("new-announcement-count/", views.new_announcement_count),




    # path('chat/', views.user_chat, name='user_chat'),
    # path('ajax/get-messages/', views.get_messages_user, name='get_messages_user'),
    # path('ajax/unread-count/', views.get_user_unread_count, name='user_unread_count'),



     path('chat/', views.user_chat, name='user_chat'),

    # ✅ AJAX endpoints
    path('ajax/unread-count/',       views.get_user_unread_count,          name='user_unread_count'),
    path('ajax/announcement-count/', views.user_announcement_unread_count, name='user_announcement_count'),

    
]