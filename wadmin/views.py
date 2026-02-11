from django.shortcuts import render

# Create your views here.
from wadmin.models import *


def home(request):
    return render(request,"admin/Home.html")