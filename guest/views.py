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

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_count = User.objects.filter(email=email, password=password).count()

        if user_count > 0:
            user = User.objects.get(email=email, password=password)
            request.session['uid'] = user.id
            return redirect('webuser:home')   # change if needed
        else:
            return render(request, "Guest/Login.html", {
                "error": "Invalid email or password"
            })

    return render(request, "Guest/Login.html")


def home(request):
    return render(request,"Guest/Home.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        admin_count = Admin.objects.filter(username=username, password=password).count()

        if admin_count > 0:
            admin = Admin.objects.get(username=username, password=password)
            request.session['aid'] = admin.id
            return redirect('wadmin:Home')   # change url name if needed
        else:
            return render(request, "Guest/Login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "Guest/Login.html")
