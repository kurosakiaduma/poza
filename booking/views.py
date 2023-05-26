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
    """
    Returns a list of weekdays in the next given number of days.

    Parameters:
    days (int): The number of days to look ahead.

    Returns:
    list: A list of dates in the format '%Y-%m-%d' that are not Friday or Sunday.

    """    
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
    """
    Returns a list of valid workdays for a given service and times.

    Parameters:
    x (list): A list of dates in the format '%Y-%m-%d'.
    service (str): The name of the service to check.
    times (dict): A dictionary with keys as weekdays and values as lists of time slots.

    Returns:
    list: A list of strings with the format 'date weekday time' for each valid workday.

    """
    validWorkdays = []
    for j in x:
        if datetime.strptime(j, '%Y-%m-%d').strftime('%A') in times.keys():
            if Appointment.objects.filter(day=j, service=service ).count() < len(times[datetime.strptime(j, '%Y-%m-%d').strftime('%A')]):
                for i in times[datetime.strptime(j, '%Y-%m-%d').strftime('%A')]:
                    # Get the current date and time
                    now = datetime.now()
                    # Convert the string in the list to a datetime object
                    dt = datetime.strptime(f'{j} {i}', '%Y-%m-%d %I:%M %p')
                    # Check if the current date and time is greater than the date and time in the list
                    if now > dt:
                        # Skip appending it to the list
                        continue
                    if Appointment.objects.filter(day=j, service=service, time=i).count() < 1:
                        validWorkdays.append(f'{j} {datetime.strptime(j, "%Y-%m-%d").strftime("%A")} {i}')
    return validWorkdays

def service_times(service):
    """
    Returns a dictionary of available times for a given service.

    Parameters:
    service (str): The name of the service to check.

    Returns:
    dict: A dictionary with keys as weekdays and values as lists of time slots.

    Raises:
    ValueError: If the service is not valid or not found.
    """    
    # Handling timing logic for each service
    if service == "Nephrology":
        times = {
                "Monday": ["11:30 AM"],
                "Wednesday": ["2:00 PM"]
                }
    elif service == "Dermatology":
            times = {
                "Tuesday": ["2:00 PM"]
                }
    elif service in ["Anaesthesia and Critical Care Medicine"]:
            times = {
                "Wednesday": ["9:00 AM","2:00 PM"]
                }
    elif service in ["Adult Neurology"]:
            times = {
                "Wednesday": ["9:00 AM","2:00 PM"]
                }
    elif service == "Interventional Cardiology":
            times = {
                "Saturday": ["10:00 AM"]
                }
    elif service == "Anaesthesia":
            times = {
                "Thursday": ["11:00 AM"]
                }
    elif service == "Radiology":
            times = {
                "Thursday": ["10:00 AM"]
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
                "Tuesday": ["2:00 PM"]
                }
    elif service == "Ear, Nose and Throat (ENT)":
            times = {
                "Monday": ["10:00 AM"],
                "Tuesday":["2:00 PM"],
                "Wednesday": ["2:00 PM"],
                "Saturday":["9:00 AM"]
                }
    elif service == "Physician / Internal Medicine":
            times = {
                "Monday": ["10:00 AM"],
                "Thursday": ["9:00 AM", "11 AM"],
                "Saturday": ["2:00 PM"]
                }
    elif service == "Paediatrics and Child Health":
            times = {
                "Monday": ["8:00 AM"],
                "Tuesday": ["9:00 AM"],
                "Wednesday": ["10:00 AM"],
                "Thursday": ["8:00 AM"]
                }
    elif service == "Adult Cardiology":
            times = {
                "Thursday": ["8:00 AM", "12:00 PM"],
                "Saturday": ["2:00 PM"]
            }
    elif service == "Pain Management":
            times = {
                "Thursday": ["11:00 AM"]
            }
    elif service == "Gynaecology / Laparoscopic / Obsterics":
            times = {
                "Monday": ["10:00 AM"],
                "Tuesday": ["9:00 AM"]
            }
        
    return times    

def index(request):
    return render(request, "index.html",{})

def assign_doctor(appears, doctors):
    """
    This function takes in two arguments:
    - appears: a dictionary containing the frequency of each doctor's appearance in existing appointments
    - doctors: a list of available doctors for the selected service.
    - The function returns the name of the assigned doctor as a string.
    """
    
    # Loop through the items in the 'appears' dictionary
    for i, j in appears.items():
        # Check if the length of the 'appears' dictionary is 1
        if len(list(appears.keys())) == 1:
            # If it is, break out of the loop
            break
        # Check if the current value is not equal to the minimum value in the 'appears' dictionary
        if j != min(appears.values()):
            # If it is not, try to remove the current key from the 'doctors' list
            try:
                doctors.remove(i)
            except ValueError:
                # If the key is not in the 'doctors' list, ignore the error
                pass
    
    # Check if the length of the 'doctors' list is 1
    if len(doctors) == 1:
        # If it is, assign the first (and only) doctor in the list as the assigned doctor
        assigned_doctor = doctors[0]
    else:
        # If it is not, try to randomly select an index from the 'doctors' list
        try:
            from random import randint
            idx = randint(0, (len(doctors)-1))
            print(f"THIS IS THE IDX ==>{idx}")
            assigned_doctor = doctors[idx]
        except IndexError:
            # If an IndexError occurs, ignore it
            pass
    
    # Return the name of the assigned doctor as a string
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
    """
    This function handles the submission of a booking request.
    :param request: The HTTP request object
    """
    user = request.user  # Get the current user from the request object

    # Calculate the minimum and maximum dates for booking
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    # Get stored data from django session:
    service = request.session.get('service')
    validWorkdays = request.session.get('validWorkdays')
    assigned_doctor = ""

    # Calculate the price for the selected service and store it in the session
    price = pricing(service)
    request.session['price'] = price
    print(f"{request.session['price']}")

    if request.method == 'POST':
        # Obtain all information data from objects pertaining to the same service
        appointments = Appointment.objects.filter(service=service)

        # Retrieve Doctor names from the filtered Doctor objects
        doctors= []
        service_doctors = Doctor.objects.filter(role=service).values_list("name")
        appears = appointments.values_list('assigned_doctor').annotate(frequency=Count('assigned_doctor'))

        for doctor in service_doctors:
            doctors.append(doctor[0])

        print(f"THE APPOINTMENT FORMAT {appointments}, \nTHE DOCTORS ARE:{doctors}")

        appears = dict(appears)

        # Assign a doctor to the appointment using the assign_doctor function
        assigned_doctor = assign_doctor(appears=appears, doctors=doctors)

        print(f"{appears} {doctors}\nASSIGNED DOCTOR-> {assigned_doctor}")

        # Get the selected date, day and time from the submitted form data
        date_day_time = request.POST.get('date_day_time')
        date = date_day_time.split()[0]
        day = date_day_time.split()[1]
        time = " ".join(s for s in date_day_time.split()[2:])
        print(f"{date_day_time.split()} {date} {time}")

        if service != None:
            if date <= maxDate and date >= minDate:
                if day != "Friday" and day != "Sunday":
                    if Appointment.objects.filter(service=service, day=date, time=time).count() < 1:
                        # Create a new Appointment object using get_or_create method
                        AppointmentForm = Appointment.objects.get_or_create(
                            service=service,
                            day=date,
                            time=time,
                            assigned_doctor=assigned_doctor,
                            uuid=user,
                            price=price
                        )
                        validWorkdays.remove(date + ' ' + day + ' ' + time)
                        messages.success(request, "Appointment Saved!")
                        render(request, 'index.html', )
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
        'service': service,
        'price': price,
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
    """
    Updates the user's appointment details and assigns a doctor.

    Parameters:
    request (HttpRequest): The request object that contains the user and session data.
    app_id (int): The id of the appointment to be updated.

    Returns:
    HttpResponse: A redirect to the user panel or a warning message if the update is not possible.

    """
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
    """
    Handles the staff panel actions and displays the appointments.

    Parameters:
    request (HttpRequest): The request object that contains the user and session data.
    **extra_fields: Optional keyword arguments that can contain the app_id or the past flag.

    Returns:
    HttpResponse: A redirect to the staff panel or the past appointments page, or a message if an action is performed.

    """
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
    """
    Renders the analytics page for the admin user.

    Parameters:
    request (HttpRequest): The request object that contains the user and session data.

    Returns:
    HttpResponse: A render of the analytics.html template with the users' and appointments' plot data.

    """
    # Get the user object from request
    user = request.user
    
    # If the user is not admin, redirect them to the home page.
    if user.account_type != "ADMIN":
        messages.error(request, "Invalid request!")
        return redirect("index")
    
    appointments = Appointment.objects.all().values()
    personas = Persona.objects.all().values()
    import pandas as pd
    import plotly.express as px
    import pytz
    # Select palette of colors
    colors = px.colors.qualitative.Plotly[:20]
    
    # Create dataframe from queryset of appointments objects
    df = pd.DataFrame.from_records(appointments)
    
    # Create dataframe from queryset of personas objects
    df_personas = pd.DataFrame.from_records(personas)

    # Filter the users dataframe to keep only the rows where account_type is “PATIENT”
    patients = df_personas[df_personas["account_type"] == "PATIENT"]
    
    # Group the patients dataframe by date_joined and count the number of users for each date:
    patients_count = patients.groupby("date_joined")["uuid"].count().cumsum().reset_index()
        
    fig = px.line(patients_count, x="date_joined", y="uuid", title="Patient Users Sign-Ups",
                  template="plotly_dark", line_shape='spline',
                  labels={"uuid":"Patient Sign-Ups", "date_joined": "Datetime"},
                  render_mode='svg', color_discrete_sequence=['#F63366'])

    fig.update_traces(mode='markers+lines', marker=dict(size=8))

    fig.update_layout(title_font=dict(size=24), xaxis_title_font=dict(size=18))
    plot_patients = fig.to_html(full_html=False)
    
    # Convert the time column to time datatype
    df['time'] = pd.to_datetime(df['time'], format='%I:%M %p').dt.time

    # Combine the day and time columns into a single column of datetime type
    df['datetime'] = pd.to_datetime(df['day'].astype(str) + " " + df['time'].astype(str), format='%Y-%m-%d %H:%M:%S')   
    # Print the dataframe with the new datetime column
    print(f"{df_personas}\n{df_personas.info()}")
    
    # Group the data by day and sum the prices for each day
    df_grouped = df.groupby('day').agg({'price': 'sum'}).reset_index()

    # Create a line plot of the total price by day
    fig = px.line(df_grouped, x='day', y='price', title='Total Revenue per Day',
                template='plotly_dark', hover_data=['price'],
                text='price', labels={'price': 'Price (KES)'},
                line_shape='spline', render_mode='svg',
                color_discrete_sequence=['#F63366'])

    fig.update_traces(mode='markers+lines', marker=dict(size=8))

    fig.update_layout(title_font=dict(size=24), xaxis_title_font=dict(size=18),
                    yaxis_title_font=dict(size=18), legend=dict(font=dict(size=16)))
    plot_div = fig.to_html(full_html=False)

    # Create a bar plot of appointments by service
    fig = px.bar(df, x="day", color = "service", template="plotly_dark",
                title="Appointments by Service", labels={"day": "Day of the Week"})
    plot_script = fig.to_html(full_html=False)

    
    # Create a pie chart showing appointments by service
    fig = px.pie(df, names="service", title="Appointments by Service", template="plotly_dark",
    color_discrete_sequence=colors, hole=0.2, hover_data=['price'],
    labels={'service': 'Service'})
    # Set textinfo attribute to show both label and percentage on pie chart
    fig.update_traces(textinfo='label+percent', pull=[0, 0.1, 0], opacity=0.8)
    # Remove legend and make pie chart a bit larger
    fig.update_layout(showlegend=False, margin=dict(l=100, r=100))
    # Convert figure to HTML
    plot_pie_dist = fig.to_html(full_html=False)


    # Create a 3D scatter plot showing price distribution by day and service
    fig = px.scatter_3d(df, x="day", y="service", z="price",
    template="plotly_dark", title="Price Distribution by Day and Service",
    labels={"day": "Day of the Week"}, symbol='service')
    # Set fixed marker size for all data points
    fig.update_traces(marker=dict(size=5))
    # Convert figure to HTML
    plot_box_dist = fig.to_html(full_html=False)


    
    # Group the data by day and service and calculate the average price for each group
    df_grouped = df.groupby(["day", "service"]).mean().reset_index()

    # Create a bar chart showing the average price for each service on each day of the week
    fig = px.bar(df_grouped, x="day", y="price", color="service", template="plotly_dark",
                title="Average Price by Service and Day of the Week", labels={"price": "Price (KES)"})
    plot_bar_day_service = fig.to_html(full_html=False)

    # Create a new column that indicates whether an appointment was completed or not
    df["completed"] = df["completed"].astype(int)

    # Group the data by day and service and calculate the percentage of appointments that were completed for each group
    df_grouped = df.groupby(["day", "service"]).mean().reset_index()

    # Create a pie chart showing the percentage of appointments that were completed for each service on each day of the week
    fig = px.pie(df_grouped, names="service", values="completed", color="service", template="plotly_dark",
                title="Percentage of Completed Appointments by Service and Day")
    plot_pie_completed = fig.to_html(full_html=False)


    # Convert the timezone-naive datetime object to a timezone-aware datetime object
    df["datetime"] = df["datetime"].apply(lambda x: pytz.timezone('UTC').localize(x))

    # Create a new column that indicates the time between when an appointment was ordered and when it was scheduled to take place
    df["time_to_appointment"] = abs((df["time_ordered"] - df["datetime"]).dt.days)

    # Group the data by service and calculate the average time for each group
    df_grouped = df.groupby("service").mean().reset_index()

    # Create a line chart showing the average time between when an appointment was ordered and when it was scheduled to take place for each service
    fig = px.line(df_grouped, x="service", y="time_to_appointment", template="plotly_dark",
    title="Average Time Between Order and Appointment by Service",
    labels={"time_to_appointment": "Time to Appointment (Days)", "service": "Service"})
    
    plot_line_dist = fig.to_html(full_html=False)

    print(f"{df}\n{df.info()}\n{df_grouped}\n{df_grouped.info()}")
    
    # Extract the hour value from the datetime object and create a new column that indicates the time of day (morning, afternoon, evening) for each appointment
    df["datetime"] = pd.cut(df["datetime"].dt.hour,
                                bins=[0, 12, 17, 24],
                                labels=["Morning", "Afternoon", "Evening"])

    # Create a scatter plot showing the relationship between time of day and price for each service on each day of the week
    fig = px.bar(df, x="datetime", y="price", color="time", template="plotly_dark",
                    title="Price Distribution by Time of Day and Day of the Week",
                    labels={"price": "Price (KES)", "time": "Time of Day", "datetime": "Time of day"})
    plot_scatter_tod = fig.to_html(full_html=False)


    return render(request, "analytics.html", {
        "user": user,
        "appointments":appointments,
        "df": df,
        "fig": fig,
        "plot_div": plot_div,
        "plot_script": plot_script,
        "plot_pie_dist": plot_pie_dist,
        "plot_box_dist": plot_box_dist,
        "plot_bar_day_service": plot_bar_day_service,
        "plot_pie_completed": plot_pie_completed,
        "plot_scatter_tod": plot_scatter_tod,
        "plot_line_dist": plot_line_dist,
        "plot_patients": plot_patients,
    })