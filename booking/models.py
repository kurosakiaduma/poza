from django.db import models
from datetime import datetime, date
from django.core.validators import *
from django.forms import ValidationError
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from random import randint
import PIL.Image, imageio, uuid

class PatientManager(BaseUserManager):
    """ Manager for all user profiles """
    use_in_migrations = True
     
    def _create_user(self, email, password, is_superuser, birth_date, phone_no, is_staff, **extra_fields):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, is_superuser=is_superuser, birth_date=birth_date, phone_no=phone_no, is_staff=is_staff, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    def create_user(self, email, password,**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self._create_user(email=email, password=password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(email=email, password=password, birth_date=date(1990, 1, 1), phone_no="0711111111", **extra_fields)
        
        return user
'''
User-input choices for the Booking-Appointment logic
'''
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

# Restriction choices
ACCOUNT_CHOICES=(
    ("ADMIN", "ADMIN"),
    ("DOCTOR", "DOCTOR"),
    ("PATIENT", "PATIENT"),
)

# Age validator function    
def at_least_age_18(value):
    today = date.today()
    age = (
        today.year
        - value.year
        - ((today.month, today.day) < (value.month, value.year))
    )
    if age < 18:
        raise ValidationError(
            f'You are a {age} year old. Account holders should be adults who have attained at least 18 years of age.'
        )

class Persona(AbstractUser, PermissionsMixin):
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4())
    username = None
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message="Please enter a valid email address in the format"), RegexValidator(regex='^name@name.name', inverse_match=True, message="Please provide a valid email address.")])
    birth_date = models.DateField(null=False, validators=[at_least_age_18])
    gender = models.CharField(choices=GENDER_CHOICES, default="Prefer Not To Say", max_length=20)
    phone_no = models.IntegerField(null=False)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES, default='PATIENT')
    kin_name = models.CharField(max_length=50, help_text="*Optional", null=True, blank=True)
    kin_contact = models.IntegerField(help_text="*Optional", null=True, blank=True)
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=8, message="Please ensure the password is at least 8 characters"), RegexValidator(regex='^password', inverse_match=True, message="Please use a different password")], default="password")
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(_('last updated'), auto_now=True)

    objects = PatientManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    def __str__(self):
        return self.email    


class Doctor(Persona):
    account_type = ACCOUNT_CHOICES[1]
    role = models.CharField(max_length=50, choices=SERVICE_CHOICES, null=False)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('doctor-detail', kwargs={'pk': self.uuid})


class Appointment(models.Model):
    uuid = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)
    app_id = models.BigAutoField(primary_key=True, default="0")
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Physician / Internal Medicine")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    note = models.TextField(max_length=255, null=True)
    def __str__(self):
        return f"{self.user.name} | day: {self.day} | time: {self.time}"