from django.shortcuts import render,redirect ,get_object_or_404

# Create your views here.
from wadmin.models import *
from guest.models import *


def home(request):
    return render(request,"admin/Home.html")


def myprofile(request):
    data = Admin.objects.get(id=request.session['aid'])
    return render(request, "admin/Myprofile.html", {'data': data})


def addcategory(request):
    if request.method == "POST":
        name = request.POST.get("txtcat")
        MachineCategory.objects.create(category_name=name)
        return redirect("wadmin:addcategory")

    categories = MachineCategory.objects.all()
    return render(request, "admin/AddMachineCategory.html", {"categories": categories})



def editcategory(request, eid):
    category = get_object_or_404(MachineCategory, id=eid)

    if request.method == "POST":
        category.category_name = request.POST.get("txtcat")
        category.save()
        return redirect("wadmin:addcategory")

    return render(request, "admin/AddMachineCategory.html", {"cat": category})



def deletecategory(request, did):
    category = get_object_or_404(MachineCategory, id=did)
    category.delete()
    return redirect("wadmin:addcategory")


def machine(request):
    if request.method == "POST":
        cat_id = request.POST.get("category")
        name = request.POST.get("machine")
        desc = request.POST.get("description")
        img = request.FILES.get("image")

        category = MachineCategory.objects.get(id=cat_id)

        Machine.objects.create(
            category=category,
            machine_name=name,
            description=desc,
            image=img
        )

        return redirect("wadmin:machine")

    data = Machine.objects.all()
    category = MachineCategory.objects.all()

    return render(request, "admin/AddMachine.html", {
        "data": data,
        "category": category
    })


def editmachine(request, eid):
    machine = get_object_or_404(Machine, id=eid)

    if request.method == "POST":
        machine.category = MachineCategory.objects.get(
            id=request.POST.get("category")
        )
        machine.machine_name = request.POST.get("machine")
        machine.description = request.POST.get("description")

        if request.FILES.get("image"):
            machine.image = request.FILES.get("image")

        machine.save()
        return redirect("wadmin:machine")

    data = Machine.objects.all()
    category = MachineCategory.objects.all()

    return render(request, "admin/AddMachine.html", {
        "machine": machine,
        "data": data,
        "category": category
    })


def deletemachine(request, did):
    machine = get_object_or_404(Machine, id=did)
    machine.delete()
    return redirect("wadmin:machine")



def announcement(request):
    announcementdata = Announcement.objects.all()

    if request.method == "POST":

        a = Announcement.objects.filter(
            title__iexact=request.POST.get("title")
        )

        if a:
            return render(request, "Admin/AddAnnouncement.html", {
                'data': announcementdata,
                'msg': "Announcement already exists"
            })

        else:
            Announcement.objects.create(
                title=request.POST.get("title"),
                description=request.POST.get("description")
            )

        return redirect("wadmin:announcement")

    else:
        return render(request, "Admin/AddAnnouncement.html", {
            'data': announcementdata
        })
    


def editannouncement(request, eid):

    announcement = Announcement.objects.get(id=eid)
    announcementdata = Announcement.objects.all()

    if request.method == "POST":

        announcement.title = request.POST.get("title")
        announcement.description = request.POST.get("description")
        announcement.save()

        return redirect("wadmin:announcement")

    else:
        return render(request, "Admin/AddAnnouncement.html", {
            "announcement": announcement,
            "data": announcementdata
        })


def deleteannouncement(request, did):
    Announcement.objects.filter(id=did).delete()
    return redirect("wadmin:announcement")


def newusers(request):
    data = User.objects.filter(status='pending')
    return render(request, "admin/NewUsers.html", {'data': data})

def acceptuser(request, id):
    user = User.objects.get(id=id)
    user.status = 'accepted'
    user.save()
    return redirect("wadmin:newusers")

def rejectuser(request, id):
    user = User.objects.get(id=id)
    user.status = 'rejected'
    user.save()
    return redirect("wadmin:newusers")

def acceptedusers(request):
    data = User.objects.filter(status='accepted')
    return render(request, "admin/AcceptedUsers.html", {'data': data})

def rejectedusers(request):
    data = User.objects.filter(status='rejected')
    return render(request, "admin/RejectedUsers.html", {'data': data})