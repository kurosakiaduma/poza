# Generated by Django 4.1 on 2023-05-19 12:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0019_persona_last_logged"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="created_at",
        ),
        migrations.AddField(
            model_name="notification",
            name="updated_at",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="service",
            field=models.CharField(
                choices=[
                    ("Adult Cardiology", "Adult Cardiology"),
                    ("Adult Neurology", "Adult Neurology"),
                    ("Anaesthesia", "Anaesthesia"),
                    (
                        "Anaesthesia and Critical Care Medicine",
                        "Anaesthesia and Critical Care Medicine",
                    ),
                    ("Dermatology", "Dermatology"),
                    ("Ear, Nose and Throat (ENT)", "Ear, Nose and Throat (ENT)"),
                    ("General Surgery", "General Surgery"),
                    (
                        "Gynaecology / Laparoscopic / Obsterics",
                        "Gynaecology / Laparoscopic / Obsterics",
                    ),
                    ("Interventional Cardiology", "Interventional Cardiology"),
                    ("Nephrology", "Nephrology"),
                    ("Ophthalmology", "Ophthalmology"),
                    ("Paediatrics and Child Health", "Paediatrics and Child Health"),
                    ("Pain Management", "Pain Management"),
                    ("Physician /Internal Medicine", "Physician / Internal Medicine"),
                    ("Radiology", "Radiology"),
                ],
                default="Physician / Internal Medicine",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="role",
            field=models.CharField(
                choices=[
                    ("Adult Cardiology", "Adult Cardiology"),
                    ("Adult Neurology", "Adult Neurology"),
                    ("Anaesthesia", "Anaesthesia"),
                    (
                        "Anaesthesia and Critical Care Medicine",
                        "Anaesthesia and Critical Care Medicine",
                    ),
                    ("Dermatology", "Dermatology"),
                    ("Ear, Nose and Throat (ENT)", "Ear, Nose and Throat (ENT)"),
                    ("General Surgery", "General Surgery"),
                    (
                        "Gynaecology / Laparoscopic / Obsterics",
                        "Gynaecology / Laparoscopic / Obsterics",
                    ),
                    ("Interventional Cardiology", "Interventional Cardiology"),
                    ("Nephrology", "Nephrology"),
                    ("Ophthalmology", "Ophthalmology"),
                    ("Paediatrics and Child Health", "Paediatrics and Child Health"),
                    ("Pain Management", "Pain Management"),
                    ("Physician /Internal Medicine", "Physician / Internal Medicine"),
                    ("Radiology", "Radiology"),
                ],
                max_length=50,
            ),
        ),
    ]
