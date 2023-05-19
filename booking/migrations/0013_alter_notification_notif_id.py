# Generated by Django 4.1 on 2023-05-19 09:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0012_notification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="notif_id",
            field=models.UUIDField(
                default=uuid.uuid1, primary_key=True, serialize=False
            ),
        ),
    ]