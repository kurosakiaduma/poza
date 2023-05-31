from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APIClient
from .models import Appointment


class BookingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()

        

    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response

    def test_booking_view(self):
        url = reverse('booking')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response

    def test_create_appointment_view(self):
        url = reverse('create_appointment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response

    def test_validWeekday(self):
        from .views import validWeekday
        today = datetime.now()
        weekdays = validWeekday(21)
        # Add assertions to validate the weekdays list

    def test_isWeekdayValid(self):
        from .views import isWeekdayValid, service_times
        service = "Nephrology"
        times = service_times(service)
        weekdays = validWeekday(21)
        valid_workdays = isWeekdayValid(weekdays, service, times)
        # Add assertions to validate the valid_workdays list

    def test_create_appointment_api(self):
        """
        Test the creation of a new appointment through the API.
        """
        url = reverse('appointment-list')
        data = {
            'patient_name': 'John Doe',
            'service': 'Dentistry',
            'appointment_date': '2023-05-30',
            'appointment_time': '10:00',
        }
        response = self.api_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.patient_name, 'John Doe')
        self.assertEqual(appointment.service, 'Dentistry')
        self.assertEqual(appointment.appointment_date, '2023-05-30')
        self.assertEqual(appointment.appointment_time, '10:00')

class BookingDatabaseTestCase(TestCase):
    def test_appointment_creation(self):
        """
        Test the creation of a new appointment in the database.
        """
        appointment = Appointment.objects.create(
            patient_name='John Doe',
            service='Dentistry',
            appointment_date='2023-05-30',
            appointment_time='10:00',
        )
        self.assertEqual(Appointment.objects.count(), 1)
        saved_appointment = Appointment.objects.first()
        self.assertEqual(saved_appointment.patient_name, 'John Doe')
        self.assertEqual(saved_appointment.service, 'Dentistry')
        self.assertEqual(saved_appointment.appointment_date, '2023-05-30')
        self.assertEqual(saved_appointment.appointment_time, '10:00')
2