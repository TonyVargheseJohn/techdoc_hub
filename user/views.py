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
        return render(request, "user/Editprofile.html", {'data': data})
