# Generated by Django 4.1 on 2023-05-17 14:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0007_appointment_assigned_doctor_alter_appointment_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="persona",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.UUID("19a11be3-4d55-43c3-99ea-949e9ee5961d"),
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
