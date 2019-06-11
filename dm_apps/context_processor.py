from django.conf import settings

def my_envr(request):
    # return the value you want as a dictionary. you may add multiple values in there.
    return {
        'PRODUCTION_SERVER': settings.PRODUCTION_SERVER,
        'USING_PRODUCTION_DB': settings.USING_PRODUCTION_DB,
    }