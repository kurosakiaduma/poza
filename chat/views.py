# Create your views here.
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import openai


def chat(request):
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
                questions and I'll do my best to provide you with accurate information. For every response, end with a note that the patient \
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