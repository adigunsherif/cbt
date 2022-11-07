from django.conf import settings


def siteconfigs(request):
    items = {
        "sitename": settings.SITE_NAME,
    }

    return items
