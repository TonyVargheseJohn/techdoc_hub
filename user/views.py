from django.shortcuts import render,redirect

# Create your views here.
from guest.models import *
from wadmin.models import *
from user.models import *




def home(request):
    return render(request,"user/Home.html")


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



def upload_machine_file(request):
    if request.method == "POST":
        machine_id = request.POST.get("machine_id")
        file = request.FILES.get("file")

        user_id = request.session.get("uid")   # logged user id

        machine = Machine.objects.get(id=machine_id)
        user = User.objects.get(id=user_id)

        UserMachineFile.objects.create(
            user=user,
            machine=machine,
            file=file
        )

    return redirect("webuser:viewmachine")