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
    selected_machine = None

    cat_id = request.GET.get("cat")
    machine_id = request.GET.get("machine")

    sel_cat_id = int(cat_id) if cat_id and cat_id.isdigit() else 0
    sel_machine_id = int(machine_id) if machine_id and machine_id.isdigit() else 0

    if cat_id:
        machines = Machine.objects.filter(category_id=cat_id)
        
    if machine_id and cat_id:
        try:
            selected_machine = Machine.objects.get(id=machine_id, category_id=cat_id)
        except Machine.DoesNotExist:
            pass

    return render(request, "User/ViewMachine.html", {
        "category": categorydata,
        "machines": machines,
        "selected_machine": selected_machine,
        "sel_cat_id": sel_cat_id,
        "sel_machine_id": sel_machine_id
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