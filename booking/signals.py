from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Appointment, Notification
from datetime import datetime
import pytz

@receiver(pre_save, sender=Appointment)
@receiver(post_save, sender=Appointment)
def appointment_updated(sender, instance, **kwargs):
    """
    Sends a notification to all related personas when an appointment is updated.

    Args:
        sender (Appointment): The sender of the signal.
        instance (Appointment): The instance of the appointment that was updated.
        **kwargs: Additional keyword arguments.
    """
    if instance.note and instance.assigned_doctor:
        persona_id = instance.uuid
        # Send notification to persona here
        message = f"Dr. {instance.assigned_doctor} updated your note for {instance.service}\nRef No: {instance.app_id}."
        """
        Update the last activity time for the current user.

        Args:
        request (HttpRequest): The current HTTP request.
        """
        # Get the Nairobi timezone object
        import pytz
        nairobi_tz = pytz.timezone('Africa/Nairobi')
        updated_at = datetime.now(nairobi_tz)
        # Send message to persona here
        # Get the notification object for this appointment
        
        notification, created = Notification.objects.get_or_create(
            notif_id=instance.app_id,
        )
        
        '''Debug line'''
        print(f"{notification} <=== SIGNAL HALFWAY")
        
        if notification.persona_id:
            notification.message = message
            notification.updated_at = updated_at
        else:
            import uuid
            notification.notif_id = uuid.uuid1()
            notification.persona_id = instance.uuid
            notification.message = message
            notification.updated_at = updated_at
        
        '''Catching errors in case notification is not created'''
        try:
            notification.save()
            print('Notification created!')
        except Exception as e:
            print(f'Error creating notification: {e}')
        
        print(f" {notification} <=== SIGNAL FINISHED")
