from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def my_envr(request):
    # return the value you want as a dictionary. you may add multiple values in there.
    return {
        # 'PRODUCTION_SERVER': settings.PRODUCTION_SERVER,
        'DB_MODE': settings.DB_MODE,
        'USE_LOCAL_DB': settings.USE_LOCAL_DB,
        'DB_NAME': settings.DB_NAME,
        'DB_HOST': settings.DB_HOST,
        'AZURE_AD': settings.AZURE_AD,
        'FAKE_TRAVEL_APP': settings.FAKE_TRAVEL_APP,
        'SITE_FULL_URL': f'https://{get_current_site(request).domain}' if request.is_secure() else f'http://{get_current_site(request).domain}',
        'DEBUG': settings.DEBUG,
    }
