# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from booking.models import Appointment

import openai


def chat(request):
    from datetime import datetime, timedelta
    from django.db.models import Count
    
    user = request.user
    maxDate = datetime.today()
    minDate = datetime.today() - timedelta(days=1)
    
    appointments = list(dict(Appointment.objects.filter(time_ordered__range=[minDate, maxDate]).values_list('uuid').annotate(frequency = Count('uuid'))).keys())
    status = [str(user.uuid) in str(app) for app in appointments]
    
    if True in status or user.account_type == "DOCTOR":
        pass
    else:
        messages.warning(request, "You don't have access to MediBot. Access is limited to users who have made appointment in the last 24 hours.")
        return redirect("http://127.0.0.1:8000/")
    chats = Chat.objects.all()
    
    return render(request, 'chat.html', {
        'chats': chats,
    })
    
    
    


@csrf_exempt
def Ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': # Check if request is Ajax

        text = request.POST.get('text')
        print(text)

        openai.api_key = "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"
        res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''You are MediBot, a chatbot curated to only provide factual responses related to medical topics or \
                questions and you'lldo your best to provide users with accurate and factual information. For every response, end with a note that the patient \
                    must always show up for any scheduled appointments to receive quality care at the hands of qualified physicians.'''},
            {"role": "user", "content": f"{text}"}
        ],
        temperature = 0 # this value depicts the randomness of the model's output
        )

        response = res.choices[0].message["content"]
        print(response)

        chat = Chat.objects.create(
            text = text,
            gpt = response
        )

        return JsonResponse({'data': response,})
    return JsonResponse({})