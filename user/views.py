from django.shortcuts import render

# Create your views here.
from user.models import *


def home(request):
    return render(request,"user/Home.html")