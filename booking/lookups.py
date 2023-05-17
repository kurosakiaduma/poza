from ajax_select import register, LookupChannel
from .models import Appointment

@register('appointments')
class AppointmentsLookUp(LookupChannel):
    
    model = Appointment
    
    def get_query(self, q, request):
        return self.model.objects.filter(app_id__icontains=q).order_by('app_id')[:21]
    
    def format_item_display(self, item):
        return u"<span class='appointment'>%s</span>" % item.app_id