from django.middleware.csrf import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Utilizador, Empresa
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
        loc = []
        c = []
        titles = Emprego.objects.filter(title__contains=title)
        for t in titles:
            jobs.append([t.title, JOB_SECTOR[int(t.job_sector) - 1][1],LOCATION[int(t.location-1)][1],t.description])
            logger.info(t)
        params = {
            'title': title,
            'jobs': jobs,
            'error': False,
            'NoTitle': False,
            'NoCategory': True,
            'NoLocation': True,
        }

        return render(request, "job_list.html", params)

    # CATEGORY
    elif category and not title and not location:
        logger.info("Only category")
        jobs = []
        cat = JOB_SECTOR[int(category)-1][1]
        for e in Emprego.objects.all():
            logger.info(e.job_sector)
            if str(e.job_sector) == category:
                jobs.append([e.title, cat , LOCATION[int(e.location)-1][1], e.description])

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
    elif location and not title and not category:
        logger.info("Only Location")
        jobs = []
        c = []
        loc = LOCATION[int(location)-1][1]

        for e in Emprego.objects.all():
            a = e.location
            if str(e.location) == location:
                logger.info(e)
                jobs.append([e.title, JOB_SECTOR[int(e.job_sector)-1][1], loc, e.description])

        logger.info(jobs)
        params = {
            'jobs': jobs,
            'location': loc,
            'error': False,
            'NoCategory': True,
            'NoTitle': True,
            'NoLocation': False
        }

        return render(request, "job_list.html", params)

    # TITLE && CATEGORY
    elif title and category and not location:
        categories = []
        jobs = []
        locations = []
        logger.info("Both title and category")
        titles = Emprego.objects.filter(title__contains=title)

        # Getting Category Name
        cat = JOB_SECTOR[int(category) - 1][1]

        # If job's category matches the request -> add to list
        for e in titles:
            if str(cat) == str(e.job_sector):
                jobs.append([e.title, cat, LOCATION[int(e.location)-1][1], e.description])

        params = {
            'jobs': jobs,
            'title': title,
            'category': cat,
            'error': False,
            'NoLocation':True,
            'NoCategory': False,
            'NoTitle': False
        }

        return render(request, "job_list.html", params)

    # TITLE && LOCATION
    elif title and not category and location:
        categories = []
        jobs = []
        logger.info("Both title and location")
        titles = Emprego.objects.filter(title__contains=title)
        
        loc = LOCATION[int(location)-1][1]
        
        for e in titles:
            c = e.job_sector
            if str(e.location) == str(location):
                jobs.append([e.title,JOB_SECTOR[int(c)-1][1],loc,e.description])
        
        params = {
            'jobs': jobs,
            'title': title,
            'location': loc,
            'error': False,
            'NoCategory': True,
            'NoTitle': False,
            'NoLocation': False,
        }

        return render(request, "job_list.html", params)

    # CATEGORY && LOCATION
    elif not title and category and location:
        jobs = []
        loc = LOCATION[int(location) - 1][1]
        cat = JOB_SECTOR[int(category)-1][1]
        
        for e in Emprego.objects.all():
            if str(e.location) == str(location) and str(e.job_sector) == category:
                jobs.append([e.title, cat, loc, e.description])

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

    # ALL
    elif title and category and location:
        jobs = []
        logger.info("Both category and location")
        titles = Emprego.objects.filter(title__contains=title)

        loc = LOCATION[int(location) - 1][1]
        cat = JOB_SECTOR[int(category) - 1][1]

        for e in titles:
            if str(e.location) == location and str(e.job_sector) == category:
                jobs.append([e.title, cat, loc, e.description])

        params = {
            'jobs': jobs,
            'title': title,
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
        if request.method == "POST":
            jobs = []
            for e in Emprego.objects.all():
                jobs.append([e.title, JOB_SECTOR[int(e.job_sector)-1][1], LOCATION[int(e.location)-1][1], e.description])
            params = {
                'title': "ALL",
                'jobs': jobs,
                'NoTitle': False,
                'NoCategory': True,
                'NoLocation': True,
                'error': False,
            }
            return render(request, "job_list.html", params)

    params = {
        'error': False
        }
    return render(request, "index.html", params)


def joblistview(request):
        jobs = []
        logger.info("Both category and location")
        j = Emprego.objects.all()

        for e in j:
            loc = LOCATION[int(e.location) - 1][1]
            cat = JOB_SECTOR[int(e.job_sector) - 1][1]
            jobs.append([e.title, cat, loc, e.description])

        params = {
            'jobs': jobs,
        }
        return render(request, 'job_all.html', params)


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
        'p_form': p_form,
        'utilizador': Utilizador
    }
    return render(request, 'profile.html', context)

def viewEmpregos(request):
    jobs = Emprego.objects.all()
    categories = []
    locations = []
    for job in jobs:
        categories.append(JOB_SECTOR[(job.job_sector-1)][1])
        locations.append(LOCATION[job.location-1][1])


    params = {
        'empregos' : Emprego.objects.all(),
        'categories' : categories,
        'ALL': True
    }
    render(request,'job_list.html',params)