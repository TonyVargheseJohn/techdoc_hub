from django.shortcuts import render,redirect

# Create your views here.
from guest.models import *


def home(request):
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        return render(request,"user/Home.html", {'user': user})
    else:
        return redirect("guest:login")


def myprofile(request):
    data = User.objects.get(id=request.session['uid'])
    return render(request, "user/Myprofile.html", {'data': data})


def editprofile(request):
    data = User.objects.get(id=request.session['uid'])
    if request.method == "POST":
        data.name = request.POST.get('name')
        data.contact = request.POST.get('contact')
        data.employeid = request.POST.get('employeid')
        data.email = request.POST.get('email')
        data.save()
        return redirect("webuser:myprofile")
    else:
<<<<<<< HEAD
        return render(request, "user/Editprofile.html", {'data': data})
=======
        return render(request,"user/Editprofile.html", {'data': data})
>>>>>>> a2cf949be7ecd12d4fa2c4e34110b703d25ca535
