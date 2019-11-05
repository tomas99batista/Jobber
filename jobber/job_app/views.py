from django.middleware.csrf import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User, Empresa
from .choices import JOB_SECTOR, LOCATION
from .forms import URF
from .forms import URF , UserUpdateForm, ProfileUpdateForm


import logging

from .forms import Createjob

# Create your views here.
from job_app.models import Emprego


def main(request):
    return render(request, "index.html")

def search_job(request):
    logger.info("IN")
    params = {}
    title = False
    category = False
    location = False
    if 'title' in request.POST:
        title = request.POST['title']
        logger.info("Title: " + title)
    if 'category' in request.POST:
        if request.POST['category'] != "0":
            category = request.POST['category']
            logger.info("Category: " + category)
        else:
            category = False
    if 'location' in request.POST:
        if request.POST['location'] != "0":
            location = request.POST['location']
            logger.info("Location: " + location)
        else:
            location = False
    
    # TITLE
    if title and not category and not location:
        logger.info("Only title")
        jobs = []
        c = []
        titles = Emprego.objects.filter(title__contains=title)
        for t in titles:
            c.append([t, JOB_SECTOR[int(t.job_sector) - 1][1]])
            logger.info(t)
        params = {
            'title': title,
            'jobs': titles,
            'category_by_title': c,
            'error': False,
            'NoTitle': False,
            'NoCategory': True,
            'NoLocation': True,
        }

        return render(request, "job_list.html", params)
    # CATEGORY
    if category and not title and not location:
        logger.info("Only category")
        jobs = []
        cat = JOB_SECTOR[int(category)-1][1]
        for e in Emprego.objects.all():
            logger.info(e.job_sector)
            if e.job_sector == category:
                jobs.append(e)

        params = {
            'category': cat,
            'jobs': jobs,
            'error': False,
            'NoTitle': True,
            'NoCategory': False,
            'NoLocation': True
        }
        return render(request, "job_list.html", params)
    # LOCATION
    if location and not title and not category:
        logger.info("Only Location")
        jobs = []
        c = []
        loc = LOCATION[int(location)-1][1]
        for e in Emprego.objects.all():
            if e.location == location:
                jobs.append(e)

        logger.info(location + ": " + loc)

        for l in jobs:
            c.append([l, JOB_SECTOR[int(l.job_sector)-1][1]])

        params = {
            'jobs': jobs,
            'location': loc,
            'categories': c,
            'error': False,
            'NoCategory': True,
            'NoTitle': True,
            'NoLocation': False
        }

        return render(request, "job_list.html", params)
    # TITLE && CATEGORY
    if title and category and not location:
        categories = []
        jobs = []
        locations = []
        logger.info("Both title and category")
        titles = Emprego.objects.filter(title__contains=title)

        # Getting Category Name
        cat = JOB_SECTOR[int(category) - 1][1]

        # If job's category matches the request -> add to list
        for e in Emprego.objects.all():
            loc = e.location
            if cat == e.job_sector:
                categories.append(e)
                locations.append(LOCATION[loc-1][1])
        # Compare
        for c in categories:
            if c in titles:
                jobs.append(c)

        params = {
            'jobs': jobs,
            'title': title,
            'category': cat,
            'locations' : locations,
            'categories': categories,
            'error': False,
            'NoCategory': False,
            'NoTitle': False
        }

        return render(request, "job_list.html", params)
    # TITLE && LOCATION
    if title and not category and location:
        categories = []
        jobs = []
        logger.info("Both title and location")
        titles = Emprego.objects.filter(title__contains=title)
        
        loc = LOCATION[int(location)-1][1]
        
        for e in titles:
            c = e.job_sector
            if e.location == location:
                categories.append(JOB_SECTOR[int(c)-1][1])
                jobs.append(e)
        
        params = {
            'jobs': jobs,
            'title': title,
            'location': loc,
            'categories': categories,
            'error': False,
            'NoCategory': True,
            'NoTitle': False,
            'NoLocation': False,
        }

        return render(request, "job_list.html", params)
    # CATEGORY && LOCATION
    if not title and category and location:
        jobs = []
        logger.info("All")

        loc = LOCATION[int(location) - 1][1]
        cat = JOB_SECTOR[int(category)-1][1]
        
        for e in Emprego.objects.all():
            if e.location == location and e.job_sector == category:
                jobs.append(e)

        params = {
            'jobs': jobs,
            'location': loc,
            'category': cat,
            'error': False,
            'NoLocation': False,
            'NoCategory': False,
            'NoTitle': True
        }

        return render(request, "job_list.html", params)
    #ALL
    if title and category and location:
        jobs = []
        logger.info("Both category and location")
        titles = Emprego.objects.filter(title__contains=title)

        loc = LOCATION[int(location) - 1][1]
        cat = JOB_SECTOR[int(category) - 1][1]

        for e in titles:
            if e.location == location and e.job_sector == category:
                jobs.append(e)

        params = {
            'jobs': jobs,
            'title':title,
            'location': loc,
            'category': cat,
            'error': False,
            'NoLocation': False,
            'NoCategory': False,
            'NoTitle': False
        }

        return render(request, "job_list.html", params)
        
    # NONE
    elif not title and not category and not location:
        logger.error("ERROR: Nothing Found")
        params = {
            'error': True
        }
        return render(request, "index.html", params)

    elif not ('title' in request.POST) and not ('category' in request.POST) and not ('location' in request.POST):
        params = {
            'error': False
        }
        return render(request, "index.html", params)


def joblistview(request):
    return render(request, 'job_list.html')


def jobcreateview(request):
    if request.method == 'POST':
        form = Createjob(request.POST)
        if form.is_valid():
            # The POST request is already working, we just need the model to be finalize so we can start populating the database
            t = form.cleaned_data.get('title')
            job_sec = form.cleaned_data.get('job_sector')
            loc = form.cleaned_data.get('location')
            descript = form.cleaned_data.get('description')
            f = form.cleaned_data.get('file')
            new_job = Emprego.objects.create(title=t, job_sector=job_sec, location=loc, description=descript, file=f, publisher="Empresa")

    else:
        form = Createjob()
    return render(request, 'job_create.html', {'form': form})

# Regist user
def register(request):
    if request.method == 'POST':
        form = URF(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created. Please log in!')
            return redirect('login')
    else:
        form = URF()
    return render(request, 'register.html', {'form':form})

# Profile acc
@login_required # To enter this page, the loggin it's required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                    request.FILES, 
                                    instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)
