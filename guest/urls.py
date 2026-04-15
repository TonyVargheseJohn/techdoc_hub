
from django.urls import path
from guest import views
app_name="guest"
urlpatterns = [
    path('Login/', views.login,name="login"),
    path('user_registration/',views.user_registration,name="user_registration"),
    path('', views.home,name="Home"),


    # path("forgot-password/", views.forgot_password, name="forgot_password"),
    # path("reset-password/<uid>/<token>/", views.reset_password, name="reset_password"),

    path('forgot-password/',views.forgot_password,name="forgotpassword"),
    path('verify-otp/',views.verify_otp,name="verifyotp"),
    path('new-password/',views.new_password,name="newpassword"),
    
]