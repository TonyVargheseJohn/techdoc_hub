from django.shortcuts import render,redirect ,get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import timedelta
from django.db.models import Count
from guest.models import Message, User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from guest.models import Message
from datetime import date




# Create your views here.
from wadmin.models import *
from guest.models import *
from user.models import *



def home(request):
    """Admin home page dashboard with live statistics"""
    
    # 👥 Users Statistics
    accepted_users = User.objects.filter(status='accepted').count()
    pending_users = User.objects.filter(status='pending').count()
    total_users = User.objects.count()
    
    # ⚙️ Machines Statistics
    total_machines = Machine.objects.count()
    
    # 📁 Files Statistics ✅ ADDED
    total_files = UserMachineFile.objects.count()
    
    # 📢 Announcements Statistics ✅ ADDED
    # Auto-delete old announcements (same logic as your announcement view)
    two_days_ago = timezone.now() - timedelta(days=2)
    Announcement.objects.filter(created_at__lt=two_days_ago).delete()
    
    # Count active announcements
    active_announcements = Announcement.objects.count()
    
    context = {
        # User stats
        'total_users': total_users,
        'accepted_users': accepted_users,  # Shows "4" to match AcceptedUsers page
        'pending_users': pending_users,
        
        # Machine stats
        'total_machines': total_machines,
        
        # File stats ✅
        'total_files': total_files,
        
        # Announcement stats ✅
        'active_announcements': active_announcements,
    }
    
    return render(request, "admin/home.html", context)



def myprofile(request):
    aid = request.session.get('aid')

    if not aid:
        return redirect('guest:login')  # not logged in

    try:
        data = Admin.objects.get(id=aid)
    except Admin.DoesNotExist:
        return redirect('guest:login')  # admin not found

    return render(request, "admin/myprofile.html", {'data': data})



def editprofile(request):

    aid = request.session.get('aid')
    if not aid:
        return redirect("wadmin:login")

    try:
        data = Admin.objects.get(id=aid)
    except Admin.DoesNotExist:
        return redirect("wadmin:login")

    if request.method == "POST":
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        employeid = request.POST.get('employeid')

        # ✅ Optional: check duplicate employee ID
        if Admin.objects.exclude(id=aid).filter(employeid=employeid).exists():
            messages.error(request, "Employee ID already exists!")
            return redirect("wadmin:editprofile")

        # Save data
        data.name = name
        data.contact = contact
        data.email = email
        data.employeid = employeid
        data.save()

        messages.success(request, "Profile updated successfully")
        return redirect("wadmin:myprofile")

    return render(request, "admin/editprofile.html", {'data': data})


def changepassword(request):

    aid = request.session.get("aid")
    if not aid:
        return redirect("wadmin:login")

    try:
        admin = Admin.objects.get(id=aid)
    except Admin.DoesNotExist:
        return redirect("wadmin:login")

    if request.method == "POST":

        current = request.POST.get('currentpassword')
        new = request.POST.get('newpassword')
        confirm = request.POST.get('confirmpassword')

        # Check current password
        if current == admin.password:

            # Check new password match
            if new == confirm:

                admin.password = new
                admin.save()

                messages.success(request, "Password changed successfully")
                return redirect("wadmin:myprofile")

            else:
                messages.error(request, "New passwords do not match")

        else:
            messages.error(request, "Current password incorrect")

    return render(request, "admin/changepassword.html")




def addcategory(request):

    categorydata = MachineCategory.objects.all()

    if request.method == "POST":

        name = request.POST.get("txtcat")

        c = MachineCategory.objects.filter(
            category_name__iexact=name
        )

        if c.exists():
            messages.warning(request, "Category already exists")
        else:
            MachineCategory.objects.create(
                category_name=name
            )
            messages.success(request, "Category added successfully")

        return redirect("wadmin:addcategory")

    return render(request, "admin/addmachinecategory.html", {
        'categories': categorydata
    })




def editcategory(request, eid):
    category = get_object_or_404(MachineCategory, id=eid)

    if request.method == "POST":
        category.category_name = request.POST.get("txtcat")
        category.save()

        messages.success(request, "Category updated successfully")

        return redirect("wadmin:addcategory")

    return render(request, "admin/addmachinecategory.html", {
        "cat": category
    })




def deletecategory(request, did):

    category = get_object_or_404(MachineCategory, id=did)

    category.delete()

    messages.success(request, "Category deleted successfully")

    return redirect("wadmin:addcategory")

def machine(request):

    categorydata = MachineCategory.objects.all()
    machinedata = Machine.objects.all()

    # ---------- SEARCH ----------
    search = request.GET.get("search")

    if search:
        machinedata = Machine.objects.filter(
            Q(machine_name__icontains=search) |
            Q(category__category_name__icontains=search)
        )

    # ---------- LIVE SEARCH AJAX ----------
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            "admin/machine_table.html",
            {"data": machinedata}
        )
        return JsonResponse({"html": html})

    # ---------- ADD MACHINE ----------
    if request.method == "POST":

        cat_id = request.POST.get("category")
        name = request.POST.get("machine")
        description = request.POST.get("description")

        image = request.FILES.get("image")
        spare_manual = request.FILES.get("spare_manual")
        software_file = request.FILES.get("software_file")

        m = Machine.objects.filter(
            machine_name__icontains=name,
            category_id=cat_id
        )

        if m.exists():
            messages.warning(request, "Machine already exists in this category")
            return redirect("wadmin:machine")

        Machine.objects.create(
            category=MachineCategory.objects.get(id=cat_id),
            machine_name=name,
            description=description,
            image=image,
            spare_manual=spare_manual,
            software_file=software_file
        )

        messages.success(request, "Machine added successfully")
        return redirect("wadmin:machine")

    return render(request, "admin/addmachine.html", {
        "data": machinedata,
        "category": categorydata
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

        if request.FILES.get("spare_manual"):
            machine.spare_manual = request.FILES.get("spare_manual")

        if request.FILES.get("software_file"):
            machine.software_file = request.FILES.get("software_file")

        machine.save()

        messages.success(request, "Machine updated successfully")

        return redirect("wadmin:machine")

    data = Machine.objects.all()
    category = MachineCategory.objects.all()

    return render(request, "admin/addmachine.html", {
        "machine": machine,
        "data": data,
        "category": category
    })



def deletemachine(request, did):
    machine = get_object_or_404(Machine, id=did)

    machine.delete()

    # ✅ Popup message after delete
    messages.success(request, "Machine deleted successfully")

    return redirect("wadmin:machine")




def announcement(request):
    # 1. AUTO-DELETE LOGIC: Delete announcements older than 2 days
    two_days_ago = timezone.now() - timedelta(days=2)
    Announcement.objects.filter(created_at__lt=two_days_ago).delete()

    # Get fresh data after cleanup
    announcementdata = Announcement.objects.all().order_by('-created_at')

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # Check for duplicates
        if Announcement.objects.filter(title__iexact=title).exists():
            messages.error(request, "An announcement with this title already exists.")
        else:
            Announcement.objects.create(
                title=title,
                description=description
            )
            messages.success(request, "Announcement successfully added!")
            # Redirect to the same page to clear the form and prevent re-submission
            return redirect("wadmin:announcement")

    return render(request, "admin/addannouncement.html", {
        'data': announcementdata
    })




def editannouncement(request, eid):
    announcement = Announcement.objects.get(id=eid)
    announcementdata = Announcement.objects.all()

    if request.method == "POST":
        announcement.title = request.POST.get("title")
        announcement.description = request.POST.get("description")
        announcement.save()

        # Add the popup message here
        messages.success(request, "Announcement updated successfully!")

        return redirect("wadmin:announcement")

    else:
        return render(request, "admin/addannouncement.html", {
            "announcement": announcement,
            "data": announcementdata
        })


def deleteannouncement(request, did):
    Announcement.objects.filter(id=did).delete()
    return redirect("wadmin:announcement")


def newusers(request):
    data = User.objects.filter(status='pending')
    return render(request, "admin/newusers.html", {'data': data})





def acceptuser(request, id):
    user = User.objects.get(id=id)
    user.status = 'accepted'
    user.save()

    # send approval mail
    try:
        send_mail(
            subject="TechDocHub Account Approved ✅",
            message=f"""
Hello {user.name},

Your account has been approved by admin 🎉
You can now login to TechDocHub.

Regards,
TechDocHub Team
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        print("Mail error:", e)

    return redirect("wadmin:newusers")






def rejectuser(request, id):
    user = User.objects.get(id=id)

    if request.method == "POST":
        reason = request.POST.get("reason")

        user.status = "rejected"
        user.save()

        # send rejection mail
        try:
            send_mail(
                subject="TechDocHub Account Rejected ❌",
                message=f"""
Hello {user.name},

We regret to inform you that your registration request has been rejected.

Reason:
{reason}

If you think this is a mistake, please contact the administrator.

Regards,
TechDocHub Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print("Mail error:", e)

        return redirect("wadmin:newusers")

    return render(request,"admin/rejectuser.html",{"user":user})


def acceptedusers(request):
    data = User.objects.filter(status='accepted')
    return render(request, "admin/acceptedusers.html", {'data': data})





def rejectedusers(request):
    data = User.objects.filter(status='rejected')
    return render(request, "admin/rejectedusers.html", {'data': data})



def view_uploaded_files(request):

    # 🔐 Optional Admin Session Check (recommended)
    if not request.session.get("aid"):
        return redirect("wadmin:login")

    # 🚀 Optimized Query
    files = (
        UserMachineFile.objects
        .select_related("machine", "machine__category", "user")
        .order_by("-upload_date")
    )

    context = {
        "files": files
    }

    return render(request, "admin/viewuploads.html", context)



def delete_uploaded_file(request, id):
    file = get_object_or_404(UserMachineFile, id=id)

    if request.method == "POST":
        reason = request.POST.get("reason")

        Notification.objects.create(
            user=file.user,
            message=f"Your file for machine '{file.machine.machine_name}' was deleted. Reason: {reason}"
        )

        file.delete()

    return redirect("wadmin:view_uploaded_files")


def admin_pie_report(request):
    # Admin session check
    if not request.session.get("aid"):
        return redirect("wadmin:login")

    # Get from and to dates from GET parameters
    from_date = request.GET.get("from_date")  # e.g., '2026-03-08'
    to_date = request.GET.get("to_date")      # e.g., '2026-03-15'

    files_query = UserMachineFile.objects.select_related("machine", "machine__category")

    # DEBUG: Print to check what's coming in
    print(f"FROM DATE: {from_date}")
    print(f"TO DATE: {to_date}")
    
    # Apply date range filter if both dates are provided
    if from_date and to_date:
        # Try different filter approaches:
        
        # Approach 1: Using date range (if upload_date is datetime)
        files_query = files_query.filter(upload_date__date__range=[from_date, to_date])
        
        # OR Approach 2: If upload_date is date field
        # files_query = files_query.filter(upload_date__range=[from_date, to_date])
        
        # OR Approach 3: More explicit filtering
        # files_query = files_query.filter(
        #     upload_date__date__gte=from_date,
        #     upload_date__date__lte=to_date
        # )
    
    # DEBUG: Check count after filtering
    print(f"Total records after filter: {files_query.count()}")
    
    # Aggregate by category_name
    pie_data = (
        files_query.values('machine__category__category_name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    # DEBUG: Print the actual data
    print("PIE DATA:", list(pie_data))

    chart_labels = [item['machine__category__category_name'] for item in pie_data]
    chart_counts = [item['count'] for item in pie_data]
    
    # DEBUG: Check if we have data
    print(f"Chart labels: {chart_labels}")
    print(f"Chart counts: {chart_counts}")
    
    # Calculate summary statistics
    categories_count = len(chart_labels)
    total_uploads = sum(chart_counts) if chart_counts else 0
    max_count = max(chart_counts) if chart_counts else 0
    
    # Calculate percentage for highest category
    highest_category_percentage = 0
    if total_uploads > 0 and max_count > 0:
        highest_category_percentage = round((max_count / total_uploads) * 100, 1)
    
    # Handle empty data case
    has_data = total_uploads > 0
    if not has_data:
        chart_labels = ["No Data"]
        chart_counts = [0]

    context = {
        "chart_labels": chart_labels,
        "chart_counts": chart_counts,
        "from_date": from_date,
        "to_date": to_date,
        "categories_count": categories_count,
        "total_uploads": total_uploads,
        "max_count": max_count,
        "highest_category_percentage": highest_category_percentage,
        "has_data": has_data,
        "today_date": date.today().isoformat(),  # Pass today's date to template
    }

    return render(request, "admin/admin_pie_report.html", context)




def admin_bar_report(request):
    # Admin session check
    if not request.session.get("aid"):
        return redirect("wadmin:login")

    # Date range filter
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    files_query = UserMachineFile.objects.select_related("machine", "machine__category")

    if from_date and to_date:
        files_query = files_query.filter(upload_date__date__range=[from_date, to_date])

    # Aggregate by machine
    bar_data = (
        files_query.values('machine__machine_name')
        .annotate(count=Count('id'))
        .order_by('-count')  # Highest upload first
    )

    chart_labels = [item['machine__machine_name'] for item in bar_data]
    chart_counts = [item['count'] for item in bar_data]

    context = {
        "chart_labels": chart_labels,
        "chart_counts": chart_counts,
        "from_date": from_date,
        "to_date": to_date,
        "today_date": date.today().isoformat()  # Pass today's date to template
    }

    return render(request, "admin/admin_bar_report.html", context)

from guest.models import Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json


def admin_chat_list(request):
    from guest.models import User
    users = User.objects.filter(status='accepted')
    return render(request, 'admin/chat_users.html', {'users': users})


def admin_chat(request, user_id):
    from guest.models import User
    user     = User.objects.get(id=user_id)
    admin_id = request.session.get('aid')
    return render(request, 'admin/chat.html', {'chat_user': user, 'admin_id': admin_id})


def get_messages_admin(request):
    user_id  = int(request.GET.get('user_id'))
    admin_id = int(request.GET.get('admin_id'))

    messages = Message.objects.filter(
        sender_type='user', sender_id=user_id,
        receiver_type='admin', receiver_id=admin_id
    ) | Message.objects.filter(
        sender_type='admin', sender_id=admin_id,
        receiver_type='user', receiver_id=user_id
    )

    msgs = [
        {
            'id':          m.id,          # ← required for delete
            'sender_type': m.sender_type,
            'message':     m.message,
            'timestamp':   m.timestamp.strftime('%I:%M %p'),
        }
        for m in messages.order_by('timestamp')
    ]

    unread_count = Message.objects.filter(
        sender_type='user',
        sender_id=user_id,
        receiver_type='admin',
        receiver_id=admin_id,
        is_read=False
    ).count()

    return JsonResponse({'messages': msgs, 'unread_count': unread_count})


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Message.objects.create(
            sender_type=data['sender_type'],
            sender_id=data['sender_id'],
            receiver_type=data['receiver_type'],
            receiver_id=data['receiver_id'],
            message=data['message']
        )
        return JsonResponse({'status': 'sent'})
    return JsonResponse({'status': 'error'})


@csrf_exempt
def mark_messages_read(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Message.objects.filter(
            sender_type='user',
            sender_id=int(data['user_id']),
            receiver_type='admin',
            receiver_id=int(data['admin_id']),
            is_read=False
        ).update(is_read=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})


@csrf_exempt
def delete_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Message.objects.filter(id=data['message_id']).delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'error'})


def total_unread_count(request):
    count = Message.objects.filter(
        sender_type='user',
        receiver_type='admin',
        is_read=False
    ).count()
    return JsonResponse({'total_unread': count})


@csrf_exempt
def delete_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Message.objects.filter(id=data['message_id']).delete()
        return JsonResponse({'status': 'deleted'})