from django.shortcuts import render,redirect

# Create your views here.
from guest.models import *
from wadmin.models import *


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
        return redirect("webuser:myprofile")
    else:
        return render(request, "user/Editprofile.html", {'data': data})
<<<<<<< HEAD



def viewannouncement(request):
    announcementdata = Announcement.objects.all().order_by('-date')

    return render(request, "user/ViewAnnouncement.html", {
        'data': announcementdata
    })


def viewmachine(request):
    categorydata = MachineCategory.objects.all()
    machines = Machine.objects.none()

    if request.GET.get("cat"):
        machines = Machine.objects.filter(category_id=request.GET.get("cat"))

    return render(request, "User/ViewMachine.html", {
        "category": categorydata,
        "machines": machines
    })
=======
>>>>>>> 473de94d695a5fc0c04f16fba7be5fa64c0b1633
