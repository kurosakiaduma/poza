from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
from django.shortcuts import render,redirect
from datetime import datetime
from .forms import RegisterUserForm, RegisterDoctorForm
from booking.models import Persona

def login_user(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            print(f"{username} {password} has been authenticated as {user}.\nREQUEST.POST details --> {request.POST}")
            login(request, user, backend="members.customauthbackend.EmailAuthBackend")
            print(f"Has been logged in {user}")
            # Redirect to a success page.
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            print(f"{user} Never authenticated")
            messages.error(request, "Invalid email or password! Please try again.")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    user = request.user
    persona = Persona.objects.get(uuid=user.uuid)
    """
    Update the last activity time for the current user.

    Args:
        request (HttpRequest): The current HTTP request.
    """
    if request.user.is_authenticated:
        # Get the session key for the current user
        session_key = request.session.session_key

        # Get the session object for the current user
        session = Session.objects.get(session_key=session_key)

        # Update the last activity time for the session
         # Activate the GMT +3 timezone
         # Get the Nairobi timezone object
        import pytz
        nairobi_tz = pytz.timezone('Africa/Nairobi')

        session.last_activity = datetime.now(nairobi_tz)
        session.save()
        print(persona, session.last_activity)
    
    persona.last_logged = session.last_activity
    persona.save()
    
    
    
    logout(request)
    messages.success(request, "Sign Out Successful")
    return redirect('index')
    
def register_user(request):
    if request.method == "POST":
        if request.user.is_superuser:
            form =  RegisterDoctorForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                print(f"{username} {password}")
                user = authenticate(username=username, password = password)
                print(f"{user}")
                login(request, user)
                messages.success(request, "Sign Up Completed!")
                return redirect('index')    
        else:    
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                print(f"{username} {password}")
                user = authenticate(username=username, password = password)
                print(f"{user}")
                login(request, user)
                messages.success(request, "Sign Up Completed!")
                return redirect('index')
    else:
        if request.user.is_superuser:
            print(f"Form not valid")
            form = RegisterDoctorForm()
        else:
            form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })