from django.conf import settings
from django.shortcuts import render, redirect

from url_shortener.shortener import shortener_storage


def index(request):
    last_short_url = request.session.pop('LAST_URL_HANDLE', '')
    if last_short_url:
        last_short_url = settings.SHORT_URL_PREFIX + last_short_url
    return render(request, 'url_shortener/index.html', context={
        'last_short_url': last_short_url,
    })


def shorten_url(request):
    long_url = request.POST['long_url']
    url_handle = shortener_storage.shorten_url(long_url)
    request.session['LAST_URL_HANDLE'] = url_handle
    return redirect('index', permanent=False)
