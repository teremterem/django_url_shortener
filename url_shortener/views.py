import logging

from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

from url_shortener.shortener import shortener_storage

log = logging.getLogger(__name__)


def index(request):
    # TODO cover this function with unit test(s)
    last_short_url = request.session.pop('LAST_URL_HANDLE', '')
    if last_short_url:
        last_short_url = settings.SHORT_URL_PREFIX + last_short_url
    return render(request, 'url_shortener/index.html', context={
        'last_short_url': last_short_url,
    })


def shorten_url(request):
    # TODO cover this function with unit test(s)
    long_url = request.POST['long_url'].strip()
    if long_url:
        url_handle = shortener_storage.shorten_url(long_url)
        request.session['LAST_URL_HANDLE'] = url_handle
    return redirect('index', permanent=False)


def expand_url(request, url_handle):
    # TODO cover this function with unit test(s)
    try:
        long_url = shortener_storage.expand_url(url_handle)
        if long_url:
            return HttpResponseRedirect(long_url)
    except Exception:
        log.exception('Failed to resolve short URL with handle %s', url_handle)

    raise Http404('URL not found')
