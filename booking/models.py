from django.db import models
from datetime import datetime, date
from django.core.validators import *
from django.forms import ValidationError
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from random import randint
import PIL.Image, imageio, uuid

class PersonaManager(BaseUserManager):
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
        
        print(f"{self.extra_fields}")
        if hasattr(extra_fields, 'role'):
            user = self.create_doctor(email=email, password=password, **extra_fields)
            return user
        
        user = self._create_user(email=email, password=password, **extra_fields)
        return user
    
    def create_doctor(self, email, password, is_superuser, birth_date, phone_no, is_staff, **extra_fields):
        """ Create a new doctor profile """
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, is_superuser=is_superuser, birth_date=birth_date, phone_no=phone_no, is_staff=is_staff, account_type = ACCOUNT_CHOICES[1], **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
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
    ("Adult Cardiology", "Adult Cardiology"),
    ("Adult Neurology", "Adult Neurology"),
    ("Anaesthesia", "Anaesthesia"),
    ("Anaesthesia and Critical Care Medicine", "Anaesthesia and Critical Care Medicine"),
    ("Dermatology", "Dermatology"),
    ("Ear, Nose and Throat (ENT)", "Ear, Nose and Throat (ENT)"),
    ("General Surgery", "General Surgery"),
    ("Gynaecology / Laparoscopic / Obsterics", "Gynaecology / Laparoscopic / Obsterics"),
    ("Interventional Cardiology", "Interventional Cardiology"),
    ("Nephrology", "Nephrology"),
    ("Ophthalmology", "Ophthalmology"),
    ("Paediatrics and Child Health", "Paediatrics and Child Health"),
    ("Pain Management", "Pain Management"),
    ("Physician /Internal Medicine", "Physician / Internal Medicine"),
    ("Radiology", "Radiology"),
    )
TIME_CHOICES = (
    ("8:00 AM", "8:00 AM"),
    ("9:00 AM", "9:00 AM"),
    ("10:00 AM", "10:00 AM"),
    ("11:00 AM", "11:00 AM"),
    ("11:30 AM", "11:30 AM"),
    ("12:00 PM", "12:00 PM"),
    ("1:30 PM", "1:30 PM"),
    ("2:00 PM", "2:00 PM"),
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
    """
    Custom user model that extends Django's AbstractUser and PermissionsMixin classes.

    Args:
        AbstractUser (AbstractBaseUser): Base class for user authentication that provides the core implementation for a User model.
        PermissionsMixin (Model): Mixin class that provides fields and methods for handling permissions and groups.

    Returns:
        Persona: A new instance of the Persona model.
    """
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
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
    last_logged = models.DateTimeField(default=datetime.now)

    objects = PersonaManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    def __str__(self):
        return self.email
    
    def get_real_instance(self):
        """
        Returns the instance of the most specific subclass of this object.
        """
        for subclass in self.__class__.__subclasses__():
            try:
                return getattr(self, subclass.__name__.lower())
            except AttributeError:
                pass
        return self    


class Doctor(Persona):
    role = models.CharField(max_length=50, choices=SERVICE_CHOICES, null=False)
    image = models.ImageField(upload_to='profiles', verbose_name='Images')
    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('doctor-detail', kwargs={'uuid': self.uuid})


class Appointment(models.Model):
    uuid = models.ForeignKey(Persona, on_delete=models.CASCADE)
    app_id = models.BigAutoField(primary_key=True,)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Physician / Internal Medicine")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    assigned_doctor = models.CharField(max_length=30, editable=False)
    price = models.PositiveIntegerField()
    note = models.TextField(default="")
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.app_id}| {self.uuid.name} | {self.service} |day: {self.day} | time: {self.time}| price: {self.price} | {self.note}"

class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    notif_id = models.IntegerField(null=False)
    persona_id = models.ForeignKey(Persona, on_delete=models.CASCADE)
    message = models.TextField()
    updated_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.notif_id}| {self.persona_id} | {self.message} |day: {self.updated_at}"