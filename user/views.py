from django.shortcuts import render,redirect

# Create your views here.
from guest.models import *


def home(request):
    return render(request,"user/Home.html")


def myprofile(request):
    data = User.objects.get(id=request.session['uid'])
    return render(request, "user/Myprofile.html", {'data': data})


def editprofile(request):
    data = User.objects.get(id=request.session['uid'])
    if request.method == "POST":
        data.name = request.POST.get('txtname')
        data.contact = request.POST.get('txtcontact')
        data.employeid = request.POST.get('txtemployeid')
        data.email = request.POST.get('txtemail')
        data.save()
        return redirect("user:myprofile")
    else:
        return render(request, "webuser/Editprofile.html", {'data': data})
