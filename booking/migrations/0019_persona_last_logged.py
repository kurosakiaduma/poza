# Generated by Django 4.1 on 2023-05-19 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0018_notification_id_alter_notification_notif_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="persona",
            name="last_logged",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
