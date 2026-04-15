from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import token_generator
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
import random



# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from guest.models import *



# def user_registration(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         contact = request.POST.get('contact')
#         employeid = request.POST.get('employeid')
#         email = request.POST.get('email')
#         gender = request.POST.get('gender')
#         photo = request.FILES.get('photo')
#         password = request.POST.get('password')

#         # Save user
#         user = User(
#             name=name,
#             contact=contact,
#             employeid=employeid,
#             email=email,
#             gender=gender,
#             photo=photo,
#             password=password
#         )
#         user.save()

#         # ---------------- ADMIN EMAIL ----------------
#         try:
#             send_mail(
#                 subject="New User Registration - TechDocHub",
#                 message=f"""
# A new user has registered.

# Name: {name}
# Employee ID: {employeid}
# Email: {email}
# Contact: {contact}
# Gender: {gender}
# """,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=["tonyparnayil@gmail.com"],  # change admin email here
#                 fail_silently=False,
#             )
#         except:
#             pass


#         # ---------------- USER EMAIL ----------------
#         try:
#             send_mail(
#                 subject="Welcome to TechDocHub",
#                 message=f"""
# Hello {name},

# Welcome to TechDocHub 🎉

# Your registration was successful.
# Please wait for admin approval.

# Regards,
# TechDocHub Team
# """,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[email],
#                 fail_silently=False,
#             )
#         except:
#             pass


#         messages.success(request, "User registered successfully. Please wait for admin approval.")
#         return redirect('guest:user_registration')

#     return render(request,'Guest/Newuser.html')




def user_registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        employeid = request.POST.get('employeid')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        photo = request.FILES.get('photo')
        password = request.POST.get('password')

        # 🔴 Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Please use another email.")
            return redirect('guest:user_registration')

        # Save user
        user = User(
            name=name,
            contact=contact,
            employeid=employeid,
            email=email,
            gender=gender,
            photo=photo,
            password=password
        )
        user.save()

        # ---------------- ADMIN EMAIL ----------------
        try:
            send_mail(
                subject="New User Registration - TechDocHub",
                message=f"""
A new user has registered.

Name: {name}
Employee ID: {employeid}
Email: {email}
Contact: {contact}
Gender: {gender}
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["tonyparnayil@gmail.com"],
                fail_silently=False,
            )
        except:
            pass

        # ---------------- USER EMAIL ----------------
        try:
            send_mail(
                subject="Welcome to TechDocHub",
                message=f"""
Hello {name},

Welcome to TechDocHub 🎉

Your registration was successful.
Please wait for admin approval.

Regards,
TechDocHub Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        except:
            pass

        messages.success(request, "User registered successfully. Please wait for admin approval.")
        return redirect('guest:login')

    return render(request,'Guest/Newuser.html')


from django.shortcuts import render, redirect
from .models import User



def home(request):
    return render(request,"Guest/Home.html")


from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import User, Admin

def login(request):
    if request.method == "POST":

        usercount = User.objects.filter(
            email=request.POST.get('email'),
            password=request.POST.get('password')
        ).count()

        admincount = Admin.objects.filter(
            email=request.POST.get('email'),
            password=request.POST.get('password')
        ).count()


        if usercount > 0:
            user = User.objects.get(
                email=request.POST.get('email'),
                password=request.POST.get('password')
            )
            if user.status == 'accepted':
                request.session['uid'] = user.id
                return redirect("webuser:home")
            else:
                return render(request, "Guest/Login.html", {
                    "error": "Your account is pending verification or has been rejected."
                })


        elif admincount > 0:
            admin = Admin.objects.get(
                email=request.POST.get('email'),
                password=request.POST.get('password')
            )
            request.session['aid'] = admin.id
            return redirect("wadmin:Home")


        else:
            return render(request, "Guest/Login.html", {
                "error": "Invalid email/username or password"
            })

    else:
        return render(request, "Guest/Login.html")





def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")
        empid = request.POST.get("empid")

        user = User.objects.filter(email=email, employeid=empid).first()

        if user:

            otp = random.randint(100000,999999)

            request.session["reset_email"] = email
            request.session["reset_otp"] = str(otp)

            send_mail(
                "TechDocHub Password Reset OTP",
                f"""
Hello {user.name},

Your OTP for password reset is:

{otp}

This OTP is valid for one time use.

Regards,
TechDocHub
""",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            return redirect("guest:verifyotp")

        else:
            messages.error(request,"Invalid Email or Employee ID")

    return render(request,"Guest/Forgot.html")



def verify_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get("otp")

        if user_otp == request.session.get("reset_otp"):

            return redirect("guest:newpassword")

        else:
            messages.error(request,"Invalid OTP")

    return render(request,"Guest/VerifyOTP.html")



def new_password(request):

    if request.method == "POST":

        password = request.POST.get("password")
        email = request.session.get("reset_email")

        user = User.objects.get(email=email)

        user.password = password
        user.save()

        # Send confirmation email
        send_mail(
            "TechDocHub Password Changed",
            f"""
Hello {user.name},

Your password has been changed successfully.

If you did not perform this action, please contact support immediately.

Regards,
TechDocHub Team
""",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        # Clear session
        request.session.pop("reset_otp", None)
        request.session.pop("reset_email", None)

        messages.success(request, "Password reset successfully")

        return redirect("guest:login")

    return render(request, "Guest/NewPassword.html")