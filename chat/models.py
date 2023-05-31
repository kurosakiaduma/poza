# Create your models here.
from django.db import models

'''User-input prompts and GPT-answers
stored in the Chat model below as well as datetime for future
data analysis tasks'''
class Chat(models.Model):
    text = models.CharField(max_length=500)
    gpt = models.CharField(max_length=17000)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    