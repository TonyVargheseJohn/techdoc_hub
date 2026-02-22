
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
