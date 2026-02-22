from django.shortcuts import render,redirect ,get_object_or_404

# Create your views here.
from wadmin.models import *
from guest.models import *


def home(request):
    return render(request,"admin/Home.html")


def myprofile(request):
    data = Admin.objects.get(id=request.session['aid'])
    return render(request, "admin/Myprofile.html", {'data': data})



# def addcategory(request):
#     categorydata = MachineCategory.objects.all()
#     if request.method == "POST":
#         c = MachineCategory.objects.filter(
#             category_name__icontains=request.POST.get("txtcat")
#         )
#         if c:
#             return render(request, "admin/AddMachineCategory.html", {
#                 'categories': categorydata,
#                 'msg': "Category already exists"
#             })
#         else:
#             MachineCategory.objects.create(
#                 category_name=request.POST.get('txtcat')
#             )
#             return render(request, "admin/AddMachineCategory.html", {
#                 'categories': categorydata
#             })
#     else:
#         return render(request, "admin/AddMachineCategory.html", {
#             'categories': categorydata
#         })

def addcategory(request):
    categorydata = MachineCategory.objects.all()
    if request.method == "POST":
        name = request.POST.get("txtcat")

        c = MachineCategory.objects.filter(
            category_name__icontains=name
        )

        if c:
            return render(request, "admin/AddMachineCategory.html", {
                'categories': categorydata,
                'msg': "Category already exists"
            })
        else:
            MachineCategory.objects.create(
                category_name=name
            )

            return render(request, "admin/AddMachineCategory.html", {
                'categories': categorydata,
                'msg': "Category added successfully"
            })
    else:
        return render(request, "admin/AddMachineCategory.html", {
            'categories': categorydata
        })



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
    machinedata = Machine.objects.all()
    categorydata = MachineCategory.objects.all()

    if request.method == "POST":
        cat_id = request.POST.get("category")
        name = request.POST.get("machine")

        m = Machine.objects.filter(
            machine_name__icontains=name,
            category_id=cat_id
        )

        if m:
            return render(request, "admin/AddMachine.html", {
                'data': machinedata,
                'category': categorydata,
                'msg': "Machine already exists in this category"
            })
        else:
            Machine.objects.create(
                category=MachineCategory.objects.get(id=cat_id),
                machine_name=name,
                description=request.POST.get("description"),
                image=request.FILES.get("image"),
                spare_manual=request.FILES.get("spare_manual"),
                software_file=request.FILES.get("software_file")
            )

            return render(request, "admin/AddMachine.html", {
                'data': machinedata,
                'category': categorydata
            })
    else:
        return render(request, "admin/AddMachine.html", {
            'data': machinedata,
            'category': categorydata
        })



def editmachine(request, eid):
    machine = get_object_or_404(Machine, id=eid)

    if request.method == "POST":
        machine.category = MachineCategory.objects.get(
            id=request.POST.get("category")
        )
        machine.machine_name = request.POST.get("machine")
        machine.description = request.POST.get("description")

        # Image update
        if request.FILES.get("image"):
            machine.image = request.FILES.get("image")

        # Spare manual update
        if request.FILES.get("spare_manual"):
            machine.spare_manual = request.FILES.get("spare_manual")

        # Software file update
        if request.FILES.get("software_file"):
            machine.software_file = request.FILES.get("software_file")

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