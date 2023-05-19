from django.shortcuts import render, redirect
from django.db.models import Count
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import *
from django.views.decorators.csrf import csrf_exempt
from .forms import *



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
    validWorkdays = []
    for j in x:
        if datetime.strptime(j, '%Y-%m-%d').strftime('%A') in times.keys():
            if Appointment.objects.filter(day=j, service=service ).count() < len(times[datetime.strptime(j, '%Y-%m-%d').strftime('%A')]):
                for i in times[datetime.strptime(j, '%Y-%m-%d').strftime('%A')]:
                    if Appointment.objects.filter(day=j, service=service, time=i).count() < 1:
                        validWorkdays.append(f'{j} {datetime.strptime(j, "%Y-%m-%d").strftime("%A")} {i}')
    return validWorkdays

def service_times(service):
    # Handling timing logic for each service
    if service == "Nephrology":
        times = {
                "Monday": ["11:30 AM"],
                "Wednesday": ["2 PM"]
                }
    elif service == "Dermatology":
            times = {
                "Tuesday": ["2 PM"]
                }
    elif service in ["Anaesthesia and Critical Care Medicine"]:
            times = {
                "Wednesday": ["9 AM","2 PM"]
                }
    elif service in ["Adult Neurology"]:
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
                "Saturday": ["2 PM"]
            }
    elif service == "Pain Management":
            times = {
                "Thursday": ["11 AM"]
            }
    elif service == "Gynaecology / Laparoscopic / Obsterics":
            times = {
                "Monday": ["10 AM"],
                "Tuesday": ["9 AM"]
            }
        
    return times    

def index(request):
    return render(request, "index.html",{})

def assign_doctor(appears, doctors):
    """Logic for assigning a doctor. I obtain a frequency queryset from the 
        appointments object on 'assigned_doctor', filter out values that have not appeared global least
        and randomly select the the index value of the remaining values in the doctors list 
    """
    for i, j in appears.items():
        if len(list(appears.keys())) == 1:
            break
        if j != min(appears.values()):
            try:
                doctors.remove(i)
            except ValueError:
                pass
               
    if len(doctors) == 1:
        assigned_doctor = doctors[0]
    else:
        try:
            from random import randint
            idx = randint(0, (len(doctors)-1))  
            print(f"THIS IS THE IDX ==>{idx}")          
            assigned_doctor = doctors[idx]
        except IndexError:
            pass
    return assigned_doctor    

def pricing(service):
    price = 0
    #Handle pricing on a seperate thread
    if service in ["Nephrology", "Physician /Internal Medicine", "Ear, Nose and Throat (ENT)","Dermatology", "Adult Neurology", "General Surgery", "Paediatrics and Child Health", "Pain Management", "Gynaecology / Laparoscopic / Obsterics", "Ophthalmology", "Radiology"]:
        price = 2500
    elif service in ["Adult Cardiology", "Interventional Cardiology"]:
        price = 3500
    elif service in ["Anaesthesia"]:
        price = 10000
    elif service == "Anaesthesia and Critical Care Medicine":
        price = 20000
    return price


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
        
        #Calling 'service_times' to only display times for the required service
        times = service_times(service)
        
        #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
        weekdays = validWeekday(22)

        #Only show the days that are not full:
        validWorkdays = isWeekdayValid(weekdays, service, times)
        
        print(f"TIMES: {times}\nSERVICE: {service}\nVALID WORKDAYS{validWorkdays}")
        
        
        
        #Filter to retrieve only available times from each date before displaying them to the user
        appointments = Appointment.objects.filter(service=service)
        
        for item in appointments:
            print(item.service, item.assigned_doctor, item.day)
    
        if appointments.exists():    
            for item in appointments:
                appointment_date = item.day
                appointment_day = dayToWeekday(str(appointment_date))
                if appointment_date in [date.split()[0] for date in validWorkdays]:    
                    validWorkdays.remove(appointment_date+' '+appointment_day+' '+item.time)
                    pass
                
        #Store day, service and times data in django session:
        request.session['service'] = service
        request.session['times'] = times
        request.session['validWorkdays'] = validWorkdays
        
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
    service = request.session.get('service')
    validWorkdays = request.session.get('validWorkdays')
    assigned_doctor = ""
        
    price = pricing(service)
    request.session['price'] = price
    print(f"{request.session['price']}")
    
    
    if request.method == 'POST':
        #Filter to retrieve only available times from each date before displaying them to the user
        appointments = Appointment.objects.filter(service=service)
        
        #Retrieve Doctor names from the filtered Doctor objects
        doctors= []
        service_doctors = Doctor.objects.filter(role=service).values_list("name") 
        appears = appointments.values_list('assigned_doctor').annotate(frequency = Count('assigned_doctor'))
        
        for doctor in service_doctors:
            doctors.append(doctor[0])

        print(f"THE APPOINTMENT FORMAT {appointments}, \nTHE DOCTORS ARE:{doctors}")
    
        appears = dict(appears)
        
        assigned_doctor = assign_doctor(appears=appears, doctors=doctors)

        print(f"{appears} {doctors}\nASSIGNED DOCTOR-> {assigned_doctor}")
        
        
        date_day_time = request.POST.get('date_day_time')
        date = date_day_time.split()[0]
        day = date_day_time.split()[1]
        time = " ".join(s for s in date_day_time.split()[2:])
        print(f"{date_day_time.split()} {date} {time}")

        if service != None:
            if date <= maxDate and date >= minDate:
                if day !="Friday" and day != "Sunday" :
                    if Appointment.objects.filter(service=service, day=date, time=time).count() < 1:
                        AppointmentForm = Appointment.objects.get_or_create(
                            service = service,
                            day = date,
                            time = time,
                            assigned_doctor = assigned_doctor,
                            uuid = user, 
                            price = price
                            )
                        validWorkdays.remove(date+' '+day+' '+time)
                        messages.success(request, "Appointment Saved!")
                        render(request, 'index.html',)
                    else:
                        messages.success(request, "The Selected Time Has Been Reserved Before!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    print(f"{date}")
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
    
    return render(request, 'bookingSubmit.html', {
        'validWorkdays': validWorkdays,
        })
@csrf_exempt
@login_required
def userPanel(request, **extra_fields):
    """
    View function that renders the user panel page with any new notifications for the user.

    Args:
        request (HttpRequest): The HTTP request object.
        extra_fields (dict): A dictionary containing any extra fields that were passed to the view.
    Returns:
        HttpResponse: The HTTP response object containing the rendered user panel page.
    """
    # Get the user object from the request
    user = request.user
    # If the user is not logged in, redirect them to the login page
    if not user.get_username():
        return render(request, 'index.html')
    
    # Split the user's name into first and last name
    name = user.name.split()
    first_name = name[0]
    last_name = name[-1]
    
    #Get the UUID of the user
    uuid = user.uuid
    
    # Initialize variables for role and image
    role = ""
    image = None
    
    # If the user is a doctor, get their role and image
    if user.account_type =="DOCTOR":
        role = Doctor.objects.get(persona_ptr_id=uuid).get_role_display()
        image = Doctor.objects.get(persona_ptr_id=uuid).image
        print(f"{image}")
    
    # Get today's date and initialize variables for minDate and maxDate
    today = datetime.today()    
    minDate = today.strftime('%Y-%m-%d')
    maxDate = (today + timedelta(days=21)).strftime('%Y-%m-%d')

    # Get all appointments for the user within the next 21 days
    appointments = Appointment.objects.filter(uuid=user, day__range=[minDate, maxDate]).order_by('app_id','day', 'time')
    
    # Get the persona object for the user and update their last_logged field
    persona = Persona.objects.get(uuid=user.uuid)
    import pytz
    nairobi_tz = pytz.timezone('Africa/Nairobi')
    persona.last_logged = datetime.now(nairobi_tz)
    persona.save()
    
    # Get all notifications for the user that have been updated since they last logged in
    notifications = Notification.objects.filter(persona_id = user, updated_at__gte=request.user.last_logged)
    
    """Debug line"""
    print(f"{appointments} {notifications} {persona}")
    
    
    if request.method == "POST":    
        today = datetime.today()

        foo = extra_fields.get('foo', None)
        
        if foo == "past":
            minDate = (today - timedelta(days=30)).strftime('%Y-%m-%d')
            maxDate = (today - timedelta(days=1)).strftime('%Y-%m-%d')
            
        else:
            minDate = today.strftime('%Y-%m-%d')
            maxDate = (today + timedelta(days=21)).strftime('%Y-%m-%d')
    
            
        #Only show the Appointments 21 days from today
        appointments = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')
            
        return render(request, 'userPanel.html', {
            "user": user,
            "name": user.name,
            'first_name': first_name,
            'last_name': last_name,
            'appointments':appointments,
            'role': role,
            'image': image,
            'notifications': notifications,
            'media_root': settings.MEDIA_ROOT
            })     
    
    return render(request, 'userPanel.html', {
        'user':user,
        'first_name': first_name,
        'last_name': last_name,
        'appointments':appointments,
        'role': role,
        'image': image,
        'notifications': notifications,
        'media_root': settings.MEDIA_ROOT
    })

def userUpdate(request, app_id):
    user = request.user
    
    appointment = Appointment.objects.get(app_id__exact=app_id)
    
    print(f"SESH: {appointment}")    
    
    userdatepicked = appointment.day
    service = appointment.service
    times = service_times(service)
    
    #Copy  booking:
    today = datetime.today()
    
    #24h check if it is possible to edit the appointment
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    if delta24:
        pass
    else:
        messages.warning(request, "You cannot edit an appointment that is due in 24 hours.")
        return redirect("userPanel")
    
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validWorkdays = isWeekdayValid(weekdays, service, times)

    #Store day and service in django session:
    request.session['service'] = service
    request.session['times'] = times
    request.session['validWorkdays'] = validWorkdays
        
    print(f"{service}...{validWorkdays}...{app_id}")
    

    if request.method == 'POST':
        #Filter to retrieve only available times from each date before displaying them to the user
        appointments = Appointment.objects.filter(service=service)
        
        #Retrieve Doctor names from the filtered Doctor objects
        doctors= []
        service_doctors = Doctor.objects.filter(role=service).values_list("name") 
        appears = appointments.values_list('assigned_doctor').annotate(frequency = Count('assigned_doctor'))
        
        for doctor in service_doctors:
            doctors.append(doctor[0])

        print(f"THE APPOINTMENT FORMAT {appointments}, \nTHE DOCTORS ARE:{doctors}")
    
        appears = dict(appears)
        
        assigned_doctor = assign_doctor(appears=appears, doctors=doctors)

        print(f"{appears} {doctors}\nASSIGNED DOCTOR-> {assigned_doctor}")
                
        date_day_time = request.POST.get('date_day_time')
        date = date_day_time.split()[0]
        time = " ".join(s for s in date_day_time.split()[2:])
        
        if Appointment.objects.filter(service=service, day=date, time=time).count() < 1:
            Appointment.objects.filter(app_id=app_id).update(
                app_id=app_id,
                uuid = user, 
                service = service,
                day = date,
                time = time,
                assigned_doctor = assigned_doctor,    
                ) 
            messages.success(request, "Appointment Edited!")
            return redirect('userPanel')
        else:
                messages.success(request, "The Selected Time Has Been Reserved Before!")
    
    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validWorkdays':validWorkdays,
            'delta24': delta24,
            'app_id': app_id,
        })


def staffPanel(request, **extra_fields):
    user = request.user
    if request.method == "POST":
        app_id =  extra_fields.get('foo', None)
        clicked_button = request.POST.get('button_id')
        if clicked_button == "complete":
            #Filter to retrieve only available times from each date before displaying them to the user            
            note = request.POST.get("note")
            patient = Appointment.objects.get(app_id=app_id).uuid.name
            Appointment.objects.filter(app_id=app_id).update(
                app_id=app_id,
                note = note,
                completed=True
                )
            appointment =  Appointment.objects.get(app_id=app_id)
            from .signals import appointment_updated
            appointment_updated(sender=Appointment, instance=appointment)
            messages.success(request, f"Completed, and sent a note to {patient}")
        elif clicked_button == "undo":
            patient = Appointment.objects.get(app_id=app_id).uuid.name
            Appointment.objects.filter(app_id=app_id).update(
                app_id=app_id,
                completed=False
            )
            messages.info(request, f"Confirmed, appointment with {patient} is not complete.")
            
        if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/staff-panel/past?':  
            return redirect("http://127.0.0.1:8000/staff-panel/past?")     
        else:
            return redirect("staffPanel")
        
    today = datetime.today()

    foo = extra_fields.get('foo', None)
    
    if foo == "past":
        minDate = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        maxDate = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        
    else:
        minDate = today.strftime('%Y-%m-%d')
        maxDate = (today + timedelta(days=21)).strftime('%Y-%m-%d')
   
        
    #Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')
        
    return render(request, 'staffPanel.html', {
        'items':items,
        "user": user,
        "name": user.name,
    })     
    
def analytics(request):
    # Get the user object from request
    user = request.user
    
    # If the user is not admin, redirect them to the home page.
    if user.account_type != "ADMIN":
        messages.error(request, "Invalid request!")
        return redirect("index")
    appointments = Appointment.objects.all().values()
    import pandas as pd
    import pdb; pdb.set_trace()
    import plotly.express as px
    
    df = pd.DataFrame.from_records(appointments)
    print(f"{df}\n{df.info()}\n{df.describe()}")
    
    return render(request, "analytics.html", {
        "user": user,
        "appointments":appointments,
        "df": df,
    })