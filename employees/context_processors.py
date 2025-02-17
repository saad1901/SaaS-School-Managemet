from .models import SchoolInfo

def school_info(request):
    return {'info': SchoolInfo.objects.first()}
