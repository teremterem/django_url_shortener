import logging

from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

from url_shortener.shortener import shortener_storage, shortener_utils

log = logging.getLogger(__name__)


def index(request):
    last_short_url = request.session.pop('LAST_URL_HANDLE', '')
    if last_short_url:
        last_short_url = settings.DJANGO_URL_SHORTENER_PREFIX + last_short_url
    return render(request, 'url_shortener/index.html', context={
        'last_short_url': last_short_url,
    })


def shorten_url(request):
    long_url = request.POST['long_url'].strip()
    if long_url:
        long_url = shortener_utils.normalize_long_url(long_url)

        url_handle = shortener_storage.shorten_url(long_url)
        request.session['LAST_URL_HANDLE'] = url_handle

    return redirect('index', permanent=False)


def expand_url(request, url_handle):
    try:
        long_url = shortener_storage.expand_url(url_handle)
        if long_url:
            return HttpResponseRedirect(long_url)
    except Exception:
        # log exception with level debug to avoid log cluttering in hypothetical production - it is easy to provoke
        # exceptions here by deliberately sending malformed url handles from the client
        log.debug('Failed to resolve short URL with handle %s', url_handle, exc_info=True)

    raise Http404('URL not found')
