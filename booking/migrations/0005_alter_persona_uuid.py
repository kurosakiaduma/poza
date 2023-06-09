# Generated by Django 4.1 on 2023-05-17 07:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0004_alter_persona_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="persona",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.UUID("7591851f-1908-4539-8a70-e953a1da29c2"),
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
