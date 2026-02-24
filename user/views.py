from django.shortcuts import render,redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
import os

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


# def viewmachine(request):
#     categorydata = MachineCategory.objects.all()
#     machines = Machine.objects.none()
#     selected_machine = None

#     cat_id = request.GET.get("cat")
#     machine_id = request.GET.get("machine")

#     sel_cat_id = int(cat_id) if cat_id and cat_id.isdigit() else 0
#     sel_machine_id = int(machine_id) if machine_id and machine_id.isdigit() else 0

#     if cat_id:
#         machines = Machine.objects.filter(category_id=cat_id)
        
#     if machine_id and cat_id:
#         try:
#             selected_machine = Machine.objects.get(id=machine_id, category_id=cat_id)
#         except Machine.DoesNotExist:
#             pass

#     return render(request, "User/ViewMachine.html", {
#         "category": categorydata,
#         "machines": machines,
#         "selected_machine": selected_machine,
#         "sel_cat_id": sel_cat_id,
#         "sel_machine_id": sel_machine_id
#     })


def viewmachine(request):

    category = MachineCategory.objects.all()
    cat_id = request.GET.get("cat")
    machine_id = request.GET.get("machine")

    machines = Machine.objects.filter(category_id=cat_id) if cat_id else []
    selected_machine = Machine.objects.filter(id=machine_id).first() if machine_id else None

    uploaded_files = None
    if selected_machine:
        uploaded_files = UserMachineFile.objects.filter(machine=selected_machine).select_related("user")

    return render(request,"user/ViewMachine.html",{
        "category":category,
        "machines":machines,
        "selected_machine":selected_machine,
        "uploaded_files":uploaded_files,
        "sel_cat_id": int(cat_id) if cat_id else None,
        "sel_machine_id": int(machine_id) if machine_id else None
    })


from django.urls import reverse

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
        url = f"{reverse('webuser:viewmachine')}?cat={machine.category.id}&machine={machine.id}"
        return redirect(url)

    return redirect("webuser:viewmachine")



def download_file(request, fid):
    try:
        file_obj = UserMachineFile.objects.get(id=fid)
        return FileResponse(file_obj.file.open('rb'), as_attachment=True)
    except UserMachineFile.DoesNotExist:
        raise Http404("File not found")
    


def my_uploads(request):
    user_id = request.session.get("uid")

    if not user_id:
        return redirect("guest:login")

    uploads = UserMachineFile.objects.filter(user_id=user_id).select_related("machine")

    search_date = request.GET.get("search_date")
    search_pdf = request.GET.get("search_pdf")
    search_machine = request.GET.get("search_machine")

    if search_date:
        uploads = uploads.filter(upload_date__date=search_date)
    if search_pdf:
        uploads = uploads.filter(file__icontains=search_pdf)
    if search_machine:
        uploads = uploads.filter(machine__machine_name__icontains=search_machine)

    return render(request, "user/MyUploads.html", {
        "uploads": uploads,
        "search_date": search_date,
        "search_pdf": search_pdf,
        "search_machine": search_machine
    })


def delete_upload(request, id):
    user_id = request.session.get("uid")

    file = get_object_or_404(UserMachineFile, id=id, user_id=user_id)

    if request.method == "POST":
        file.file.delete()   # delete file from media folder
        file.delete()        # delete record
        return redirect("webuser:my_uploads")

    return redirect("webuser:my_uploads")


def my_notifications(request):
    uid = request.session.get("uid")

    notes = Notification.objects.filter(user_id=uid).order_by("-created_at")

    return render(request,"user/Notifications.html",{"notes":notes})

def search_uploads(request):
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("guest:login")

    # Exclude files uploaded by the current user
    uploads = UserMachineFile.objects.exclude(user_id=user_id).select_related("machine", "user")

    search_date = request.GET.get("search_date")
    search_pdf = request.GET.get("search_pdf")
    search_machine = request.GET.get("search_machine")
    search_query = request.GET.get("search_query")  # From navbar quick search

    if search_query:
        # Simple global search from navbar
        uploads = uploads.filter(file__icontains=search_query) | uploads.filter(machine__machine_name__icontains=search_query)
    
    if search_date:
        uploads = uploads.filter(upload_date__date=search_date)
    if search_pdf:
        uploads = uploads.filter(file__icontains=search_pdf)
    if search_machine:
        uploads = uploads.filter(machine__machine_name__icontains=search_machine)

    return render(request, "user/SearchUploads.html", {
        "uploads": uploads,
        "search_date": search_date,
        "search_pdf": search_pdf,
        "search_machine": search_machine,
        "search_query": search_query
    })
