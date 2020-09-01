from django.shortcuts import render, redirect


def index(request):
    return render(request, 'url_shortener/index.html')


def shorten_url(request):
    # TODO
    return redirect('index', permanent=False)
