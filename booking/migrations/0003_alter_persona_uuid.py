# Generated by Django 4.1 on 2023-05-15 19:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0002_alter_appointment_service_alter_doctor_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="persona",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.UUID("d130f345-dce2-4aaa-9398-c9db775e45f8"),
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
