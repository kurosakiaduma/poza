from django.db import models
from datetime import datetime
from django.core.validators import *
from django.contrib.admin import ModelAdmin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from random import randint
import PIL.Image, imageio

SERVICE_CHOICES = (
    ("1", "Adult Cardiology"),
    ("2", "Adult Neurology"),
    ("3", "Anaesthesia"),
    ("4", "Anaesthesia and Critical Care Medicine"),
    ("5", "Dermatology"),
    ("6, Nose and Throat (ENT)", "Ear, Nose and Throat (ENT)"),
    ("7", "General Surgery"),
    ("8", "Gynaecology / Laparoscopic / Obsterics"),
    ("9", "Nephrology"),
    ("10", "Ophthalmologist"),
    ("11", "Paediatrics and Child Health"),
    ("12", "Pain Management"),
    ("13", "Physician /Internal Medicine"),
    ("14", "Radiology"),
    )
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female", "Female"),
    ("Non-Binary", "Non-Binary"),
    ("Prefer Not To Say","Prefer Not To Say")
)
    
class Patient(models.Model):
    uuid = models.CharField(max_length=10, unique=True, blank=True, null=True)
    name = models.TextField(max_length=50, null=False)
    birth_date = models.DateField(null=False, blank=True)
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message="Please enter a valid email address in the format")], default="name@name.name")
    gender = models.CharField(choices=GENDER_CHOICES, null=False, max_length=20)
    phone_no = models.IntegerField(null=False)
    account_type = models.CharField(max_length=10, default='PATIENT', editable=False)
    kin_name = models.TextField(max_length=50, null=True)
    kin_contact = models.IntegerField(null=True)
    

@receiver(post_save, sender=Patient)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(user=instance)

@receiver(post_save, sender=Patient)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Appointment(models.Model):
    uuid = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Physician / Internal Medicine")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"


class Doctor(models.Model):
    uuid = models.CharField(max_length=2, unique=True, blank=True, null=True)
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=8, message="Please ensure the password is at least 8 characters"), RegexValidator(regex='/password')], default="password")
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message="Please enter a valid email address in the format")], default="name@name.name")
    phone_no = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex='^\d{10}$', message="Please enter a 10-digit number")])
    account_type = models.CharField(max_length=10, default='DOCTOR', editable=False)
    role = models.CharField(max_length=50, choices=SERVICE_CHOICES, null=False)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while True:
            self.uuid = str(randint(1, 20))
            if Doctor.objects.filter(uuid = self.uuid).count() < 1:
                break
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('doctor-detail', kwargs={'pk': self.pk})