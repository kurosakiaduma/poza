from .models import SERVICE_DESCS

def services_processor(request):
    return {
        "service_descriptions": SERVICE_DESCS,
    }