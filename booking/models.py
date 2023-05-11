from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

SERVICE_CHOICES = (
    ("Adult Cardiology", "Adult Cardiology"),
    ("Adult Neurology", "Adult Neurology"),
    ("Anaesthesia", "Anaesthesia"),
    ("Anaesthesia and Critical Care Medicine", "Anaesthesia and Critical Care Medicine"),
    ("Dermatology", "Dermatology"),
    ("Ear, Nose and Throat (ENT)", "Ear, Nose and Throat (ENT)"),
    ("General Surgery", "General Surgery"),
    ("Gynaecology / Laparoscopic / Obsterics", "Gynaecology / Laparoscopic / Obsterics")
    ("Nephrology", "Nephrology"),
    ("Ophthalmologist", "Ophthalmologist"),
    ("Paediatrics and Child Health", "Paediatrics and Child Health"),
    ("Pain Management", "Pain Management"),
    ("Physician /Internal Medicine", "Physician /Internal Medicine"),
    ("Radiology", "Radiology"),
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

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Physician / Internal Medicine")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField()
    birth_date = models.DateField(null=True, blank=True)
    
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
