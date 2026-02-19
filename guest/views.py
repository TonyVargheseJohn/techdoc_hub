from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from guest.models import *

def user_registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        employeid = request.POST.get('employeid')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        photo = request.FILES.get('photo')
        password = request.POST.get('password')
        

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

        messages.success(request, "User registered successfully")
        return redirect('guest:user_registration')

    return render(request,'Guest/Newuser.html')


from django.shortcuts import render, redirect
from .models import User

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
            request.session['uid'] = user.id
            return redirect("webuser:home")


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


def home(request):
    return render(request,"Guest/Home.html")



