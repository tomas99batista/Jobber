from django.middleware.csrf import logger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User
from .choices import JOB_SECTOR, LOCATION
from .forms import URF
from .forms import URF , UserUpdateForm, ProfileUpdateForm


import logging

from .forms import Createjob

# Create your views here.
from job_app.models import Emprego


def main(request):
    return render(request, "index.html")

'''
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
'''

def search_job(request):
    logger.info("IN")
    title = False
    category = False
    location = False
    name = False
    city = False
    sector = False

    if 'name' in request.POST:
        name = request.POST['name']
        logger.info("Name: " + name)
    if 'sector' in request.POST:
        if request.POST['sector'] != "0":
            sector = request.POST['sector']
            logger.info("Sector: " + sector)
        else:
            category = False
    if 'city' in request.POST:
        if request.POST['city'] != "0":
            city = request.POST['city']
            logger.info("City: " + city)
        else:
            city = False
    if 'name' in request.POST:
        name = request.POST['title']
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
            'category': c,
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
        cat = JOB_SECTOR[int(category) - 1][1]
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
    elif location and not title and not category:
        logger.info("Only Location")
        jobs = []
        c = []
        loc = LOCATION[int(location) - 1][1]
        for e in Emprego.objects.all():
            if e.location == location:
                jobs.append(e)

        logger.info(location + ": " + loc)

        for l in jobs:
            c.append([l, JOB_SECTOR[int(l.job_sector) - 1][1]])

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
    elif title and category and not location:
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
                locations.append(LOCATION[loc - 1][1])
        # Compare
        for c in categories:
            if c in titles:
                jobs.append(c)

        params = {
            'jobs': jobs,
            'title': title,
            'category': cat,
            'locations': locations,
            'categories': categories,
            'error': False,
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

        loc = LOCATION[int(location) - 1][1]

        for e in titles:
            c = e.job_sector
            if e.location == location:
                categories.append(JOB_SECTOR[int(c) - 1][1])
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
    elif not title and category and location:
        jobs = []
        logger.info("All")

        loc = LOCATION[int(location) - 1][1]
        cat = JOB_SECTOR[int(category) - 1][1]

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
    # ALL
    elif title and category and location:
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
            'title': title,
            'location': loc,
            'category': cat,
            'error': False,
            'NoLocation': False,
            'NoCategory': False,
            'NoTitle': False
        }

        return render(request, "job_list.html", params)

    # NAME
    elif name and not sector and not city:
        logger.info("Only Name")
        sectors = []
        names = Emprego.objects.filter(first_name__contains=name,
                                        last_name_contains=name)

        for name in names:
            sectors.append([name, JOB_SECTOR[int(name.job_sector) - 1][1]])
            logger.info(name)

        params = {
            'name': name,
            'jobs': names,
            'sector': sectors,
            'error': False,
            'NoName': False,
            'NoSector': True,
            'NoCity': True,
        }

        return render(request, "user_list.html", params)
    # Sector
    elif sector and not name and not city:
        logger.info("Only Sector")
        users = []
        sector = JOB_SECTOR[int(sector) - 1][1]
        for e in User.objects.all():
            logger.info(e.job_sector)
            if e.sector == sector:
                users.append(e)

        params = {
            'sector': sector,
            'users': users,
            'error': False,
            'NoName': True,
            'NoSector': False,
            'NoCity': True
        }
        return render(request, "user_list.html", params)

    # CITY
    elif city and not name and not sector:
        logger.info("Only City")
        users = []
        sectors = []
        c = LOCATION[int(city) - 1][1]
        for e in Emprego.objects.all():
            if e.city == city:
                users.append(e)

        logger.info(city + ": " + c)

        for user in users:
            sectors.append([user, JOB_SECTOR[int(user.sector) - 1][1]])

        params = {
            'users': users,
            'city': city,
            'sectors': sectors,
            'error': False,
            'NoSector': True,
            'NoName': True,
            'NoCity': False
        }

        return render(request, "user_list.html", params)
    # NAME && SECTOR
    elif name and sector and not city:
        sectors = []
        users = []
        cities = []
        logger.info("Both Name and Sector")
        names = Emprego.objects.filter(first_name__contains=name,
                                        last_name_contains=name)
        # Getting Category Name
        sector = JOB_SECTOR[int(category) - 1][1]

        # If job's category matches the request -> add to list
        for user in User.objects.all():
            loc = user.location
            if sector == user.sector:
                sectors.append(sector)
                city.append(LOCATION[loc - 1][1])
        # Compare
        for c in sectors:
            if c in names:
                users.append(c)

        params = {
            'users': users,
            'name': names,
            'sector': sector,
            'city': cities,
            'sectors': sectors,
            'error': False,
            'NoSector': False,
            'NoName': False,
            'NoCity': True
        }

        return render(request, "user_list.html", params)

    # NAME && CITY
    elif name and not sector and city:
        sectors = []
        users = []
        logger.info("Both name and city")
        names = Emprego.objects.filter(first_name__contains=name,
                                        last_name_contains=name)

        city = LOCATION[int(city) - 1][1]

        for e in name:
            c = e.sector
            if e.city == city:
                sectors.append(JOB_SECTOR[int(c) - 1][1])
                users.append(e)

        params = {
            'users': users,
            'names': names,
            'city': city,
            'sectors': sectors,
            'error': False,
            'NoSector': True,
            'NoName': False,
            'NoCity': False,
        }

        return render(request, "user_list.html", params)

    # SECTOR && CITY
    elif not name and sector and city:
        users = []
        logger.info("All")

        city = LOCATION[int(city) - 1][1]
        sector = JOB_SECTOR[int(sector) - 1][1]

        for e in Emprego.objects.all():
            if e.city == city and e.sector == sector:
                users.append(e)

        params = {
            'users': users,
            'city': city,
            'sector': sector,
            'error': False,
            'NoCity': False,
            'NoSector': False,
            'NoName': True
        }

        return render(request, "user_list.html", params)

    # ALL
    elif name and sector and city:
        users = []
        logger.info("ALL")
        names = Emprego.objects.filter(first_name__contains=name,
                                       last_name_contains=name)

        city = LOCATION[int(city) - 1][1]
        sector = JOB_SECTOR[int(sector) - 1][1]

        for e in names:
            if e.city == city and e.sector == sector:
                users.append(e)

        params = {
            'users': users,
            'name': name,
            'city': city,
            'sector': sector,
            'error': False,
            'NoCity': False,
            'NoSector': False,
            'NoName': False
        }

        return render(request, "user_list.html", params)

    else:
        logger.info("NOTHING FOUND")
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
            job_info = form.cleaned_data.get('job_sector')
            print(job_info)
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