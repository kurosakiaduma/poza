from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
from .forms import AppointmentForm

def index(request):
    return render(request, "index.html",{})

def booking(request):
    """Function that applies the necessar business logic required in booking only available time slots within a 21-day period"""
    #Calling 'getServices' function to retrieve a list of all the available services
    services = getServices()
    times = {}

    if request.method == 'POST':
        service = request.POST.get('service')
        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')
        # Handling timing logic for each service
        elif service == "Nephrology":
            times = {
                "Monday": ["11:30 AM"],
                "Wednesday": ["2 PM"]
                }
        elif service == "Dermatology":
            times = {
                "Tuesday": ["2 PM"]
                }
        elif service in ["Adult Neurology", "Anaesthesia and Critical Care Medicine"]:
            times = {
                "Wednesday": ["9 AM","2 PM"]
                }
        elif service == "Interventional Cardiology":
            times = {
                "Saturday": ["10 AM"]
                }
        elif service == "Anaesthesia":
            times = {
                "Thursday": ["11 AM"]
                }
        elif service == "Radiology":
            times = {
                "Thursday": ["10 AM"]
                }
        elif service == "General Surgery":
            times = {
                "Monday": ["1:30 PM"],
                "Tuesday": ["1:30 PM"],
                "Wednesday": ["1:30 PM"],
                "Thursday": ["1:30 PM"]
                }
        elif service == "Ophthalmology":
            times = {
                "Tuesday": ["2 PM"]
                }
        elif service == "Ear, Nose and Throat (ENT)":
            times = {
                "Monday": ["10 AM"],
                "Tuesday":["2 PM"],
                "Wednesday": ["2 PM"],
                "Saturday":["9 AM"]
                }
        elif service == "Physician / Internal Medicine":
            times = {
                "Monday": ["10 AM"],
                "Thursday": ["9 AM", "11 AM"],
                "Saturday": ["2 PM"]
                }
        elif service == "Paediatrics and Child Health":
            times = {
                "Monday": ["8 AM"],
                "Tuesday": ["9 AM"],
                "Wednesday": ["10 AM"],
                "Thursday": ["8 AM"]
                }
        elif service == "Adult Cardiology":
            times = {
                "Thursday": ["8 AM", "12 PM"],
                "Friday": ["2 PM"]
            }
        elif service == "Pain Management":
            times = {
                "Thursday": ["11 AM"]
            }
        elif service == "Gynaecology / Laparoscopic / Obsterics":
            times = {
                "Monday": "10 AM",
                "Tuesday": "9 AM"
            }
        #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
        weekdays = validWeekday(22)

        #Only show the days that are not full:
        validWorkdays = isWeekdayValid(weekdays, service, times)

        #Store day and service in django session:
        request.session['service'] = service
        request.session['times'] = times
        request.session['validWorkdays'] = validWorkdays
        print(f"{service}...{validWorkdays}")
        
        return redirect('bookingSubmit')


    return render(request, 'booking.html', {
            'times': times,
            'services': services,
        })

def bookingSubmit(request):
    user = request.user
    
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    
    #Get stored data from django session:
    times = request.session.get('times')
    service = request.session.get('service')
    validWorkdays = request.session.get('validWorkdays')
    
    #Set a default day from the list of available days
    day = request.session['day']

    #Handle pricing on a seperate thread
    if service in ["Nephrology", "Physician /Internal Medicine", "Ear, Nose and Throat (ENT)","Dermatology", "Adult Neurology", "General Surgery", "Paediatrics and Child Health", "Pain Management", "Gynaecology / Laparoscopic / Obsterics", "Ophthalmologist", "Radiology"]:
        request.session['price'] = 2500
    elif service in ["Adult Cardiology", "Interventional Cardiology"]:
        request.session['price'] = 3500
    elif service in ["Anaesthesia"]:
        request.session['price'] = 10000
    elif service == "Anaesthesia and Critical Care Medicine":
        request.session['price'] = 20000
    
    price = request.session.get('price')
    print(f"{request.session['price']}")
    
    #Only show the time of the day that has not been selected before:
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date !="Friday" and date!="Sunday" :
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Appointment.objects.get_or_create(
                                service = service,
                                day = day,
                                time = time,
                                uuid = user, 
                                price = price
                            )
                            messages.success(request, "Appointment Saved!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
    
    return render(request, 'bookingSubmit.html', {
        'validWorkdays': list(validWorkdays.keys()),
        'times': list(validWorkdays.values())
    })

def userPanel(request):
    user = request.user
    name = user.name.split()
    first_name = name[0]
    last_name = name[-1]
    uuid = user.uuid
    appointments = Appointment.objects.filter(uuid=uuid).order_by('day', 'time')
    
    """Debug line"""
    print(f"{appointments} {name}")
    
    return render(request, 'userPanel.html', {
        'user':user,
        'first_name': first_name,
        'last_name': last_name,
        'appointments':appointments,
    })

def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    #Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validWorkdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('userUpdateSubmit', id=id)


    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validWorkdays':validWorkdays,
            'delta24': delta24,
            'id': id,
        })

def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            AppointmentForm = Appointment.objects.filter(pk=id).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Appointment Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })

def staffPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items':items,
    })
def getServices():
    services=[]
    for service in SERVICE_CHOICES:
        services.append(service[1])
    return services

def dayToWeekday(x):
    y = datetime.strptime(x, "%Y-%m-%d").strftime('%A')
    return y

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y not in ['Friday', 'Sunday']:
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def isWeekdayValid(x, service, times):
    validWorkdays = {}
    for j in x:
        if datetime.strptime(j, '%Y-%m-%d').strftime('%A') in times.keys():
            if Appointment.objects.filter(day=j, service=service ).count() < len(times[datetime.strptime(j, '%Y-%m-%d').strftime('%A')]):
                validWorkdays.update({f'{j+ " " + datetime.strptime(j, "%Y-%m-%d").strftime("%A")}': []})
                for i in times[datetime.strptime(j, '%Y-%m-%d').strftime('%A')]:
                    if Appointment.objects.filter(day=j, service=service, time=i).count() < 1:
                        validWorkdays[f'{j+" "+datetime.strptime(j, "%Y-%m-%d").strftime("%A")}'].append(i)
    return validWorkdays

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(app_id=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x