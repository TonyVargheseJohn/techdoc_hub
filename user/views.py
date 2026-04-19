from django.shortcuts import render,redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.http import FileResponse, Http404
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from guest.models import Message, Admin
from django.http import JsonResponse
import json

import os

# Create your views here.
from guest.models import *
from wadmin.models import *
from user.models import *




def home(request):
    return render(request,"user/home.html")




def myprofile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('guest:login')  # redirect if not logged in

    try:
        data = User.objects.get(id=uid)
    except User.DoesNotExist:
        return redirect('guest:login')  # user deleted or not found

    return render(request, 'user/myprofile.html', {'data': data})

    


def editprofile(request):
    data = User.objects.get(id=request.session['uid'])

    if request.method == "POST":
        data.name = request.POST.get('name')
        data.contact = request.POST.get('contact')
        data.employeid = request.POST.get('employeid')
        data.email = request.POST.get('email')
        data.save()

        messages.success(request, "Profile updated successfully")
        return redirect("webuser:myprofile")

    else:
        return render(request, "user/editprofile.html", {'data': data})



def changepassword(request):

    if "uid" not in request.session:
        return redirect("login")

    user = User.objects.get(id=request.session["uid"])

    if request.method == "POST":

        if request.POST.get('currentpassword') == user.password:

            if request.POST.get('newpassword') == request.POST.get('confirmpassword'):

                user.password = request.POST.get('newpassword')
                user.save()

                messages.success(request, "Password changed successfully")
                return redirect("webuser:myprofile")

            else:
                messages.error(request, "New passwords do not match")

        else:
            messages.error(request, "Current password incorrect")

    return render(request, "user/changepassword.html")



from django.http import JsonResponse
# from adminapp.models import Announcement

def new_announcement_count(request):

    last_seen = request.session.get("last_seen_announcement", 0)

    latest = Announcement.objects.order_by("-id").first()

    if latest:
        latest_id = latest.id
    else:
        latest_id = 0

    if latest_id > last_seen:
        count = Announcement.objects.filter(id__gt=last_seen).count()
    else:
        count = 0

    return JsonResponse({"count": count})


def viewannouncement(request):

    data = Announcement.objects.all().order_by("-id")

    latest = Announcement.objects.order_by("-id").first()
    if latest:
        request.session["last_seen_announcement"] = latest.id

    return render(request,"user/viewannouncement.html",{"data":data})



# def viewannouncement(request):
#     announcements = Announcement.objects.all().order_by('-created_at')
#     return render(request, "user/Viewannouncement.html", {'data': announcements})



# def new_announcement_count(request):
#     # Example: get all new announcements
#     announcements = Announcement.objects.all()
#     data = []
#     for a in announcements:
#         data.append({
#             'id': a.id,
#             'title': a.title,
#             'description': a.description,
#             'created_at': a.created_at.strftime("%Y-%m-%d %H:%M:%S")  # convert datetime to string
#         })

#     return JsonResponse({'announcements': data})



# def viewmachine(request):

#     category = MachineCategory.objects.all()
#     cat_id = request.GET.get("cat")
#     machine_id = request.GET.get("machine")

#     machines = Machine.objects.filter(category_id=cat_id) if cat_id else []
#     selected_machine = Machine.objects.filter(id=machine_id).first() if machine_id else None

#     uploaded_files = None
#     if selected_machine:
#         uploaded_files = UserMachineFile.objects.filter(machine=selected_machine).select_related("user")

#     return render(request,"user/ViewMachine.html",{
#         "category":category,
#         "machines":machines,
#         "selected_machine":selected_machine,
#         "uploaded_files":uploaded_files,
#         "sel_cat_id": int(cat_id) if cat_id else None,
#         "sel_machine_id": int(machine_id) if machine_id else None
#     })

def viewmachine(request):

    category = MachineCategory.objects.all()
    cat_id = request.GET.get("cat")
    machine_id = request.GET.get("machine")

    machines = Machine.objects.filter(category_id=cat_id) if cat_id else []
    selected_machine = Machine.objects.filter(id=machine_id).first() if machine_id else None

    uploaded_files = None
    if selected_machine:
        uploaded_files = (
            UserMachineFile.objects
            .filter(machine=selected_machine)
            .select_related("user")
            .order_by("-upload_date")  # ✅ Latest first
        )

    return render(request, "user/viewmachine.html", {
        "category": category,
        "machines": machines,
        "selected_machine": selected_machine,
        "uploaded_files": uploaded_files,
        "sel_cat_id": int(cat_id) if cat_id else None,
        "sel_machine_id": int(machine_id) if machine_id else None
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

    uploads = (
        UserMachineFile.objects
        .filter(user_id=user_id)
        .select_related("machine", "machine__category")
        .order_by("-upload_date")
    )

    # 2-hour delete permission logic
    now = timezone.now()
    for u in uploads:
        u.can_delete = u.upload_date and now <= u.upload_date + timedelta(hours=2)

    return render(request, "user/myuploads.html", {
        "uploads": uploads
    })


def search_uploads(request):
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("guest:login")

    # Exclude the logged-in user's own files
    uploads = (
        UserMachineFile.objects
        .exclude(user_id=user_id)
        .select_related("machine", "machine__category", "user")
        .order_by("-upload_date")
    )

    return render(request, "user/searchuploads.html", {
        "uploads": uploads
    })


def delete_upload(request, id):
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("guest:login")

    file = get_object_or_404(UserMachineFile, id=id, user_id=user_id)

    now = timezone.now()
    if request.method == "POST":
        if now <= file.upload_date + timedelta(hours=2):
            file.delete()

    return redirect("webuser:my_uploads")


def my_notifications(request):
    uid = request.session.get("uid")

    notes = Notification.objects.filter(user_id=uid).order_by("-created_at")

    return render(request,"user/notifications.html",{"notes":notes})





# ---------- CHAT SYSTEM ----------


def chat_page(request, uid):
    receiver = User.objects.get(id=uid)
    sender = User.objects.get(id=request.session["uid"])

    messages = ChatMessage.objects.filter(
        sender__in=[sender, receiver],
        receiver__in=[sender, receiver]
    ).order_by("timestamp")

    return render(request,"user/chat.html",{
        "receiver":receiver,
        "messages":messages
    })




def send_message(request):
    if request.method == "POST":
        sender = User.objects.get(id=request.session["uid"])
        receiver = User.objects.get(id=request.POST.get("receiver_id"))
        message = request.POST.get("message")

        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )

        return JsonResponse({"status":"sent"})
    


def fetch_messages(request, uid):
    sender = User.objects.get(id=request.session["uid"])
    receiver = User.objects.get(id=uid)

    messages = ChatMessage.objects.filter(
        sender__in=[sender, receiver],
        receiver__in=[sender, receiver]
    ).order_by("timestamp")

    data = []
    for msg in messages:
        data.append({
            "sender": msg.sender.id,
            "message": msg.message,
            "time": msg.timestamp.strftime("%H:%M")
        })

    return JsonResponse(data, safe=False)



from guest.models import User   # adjust if your model is elsewhere

def chat_users(request):
    if "uid" not in request.session:
        return redirect("guest:login")

    users = User.objects.exclude(id=request.session["uid"])
    return render(request, "user/chat_users.html", {"users": users})





def user_chat(request):
    from guest.models import Message, User
    user_id = request.session.get('uid')
    if not user_id:
        return redirect('guest:login')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('guest:login')

    # ✅ Mark all admin messages as read when user opens chat
    Message.objects.filter(
        sender_type='admin',
        receiver_type='user',
        receiver_id=user_id,
        is_read=False
    ).update(is_read=True)

    return render(request, 'user/chat.html', {'user': user})


def get_user_unread_count(request):
    from guest.models import Message
    user_id = request.session.get('uid')
    if not user_id:
        return JsonResponse({'unread_count': 0})
    unread = Message.objects.filter(
        sender_type='admin',
        receiver_type='user',
        receiver_id=user_id,
        is_read=False
    ).count()
    return JsonResponse({'unread_count': unread})


def user_announcement_unread_count(request):
    from guest.models import AnnouncementView
    from wadmin.models import Announcement
    user_id = request.session.get('uid')
    if not user_id:
        return JsonResponse({'count': 0})
    total  = Announcement.objects.count()
    viewed = AnnouncementView.objects.filter(user_id=user_id).count()
    return JsonResponse({'count': max(total - viewed, 0)})