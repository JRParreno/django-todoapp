from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):

    return render(request, 'dashboard/home.html')


def about(request):

    return render(request, 'dashboard/about.html')


def contact_us(request):

    return render(request, 'dashboard/contact_us.html')