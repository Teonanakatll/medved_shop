from django.shortcuts import render

def landing(request):
    name = "Syava"
    current_day = "05.03.1998"
    return render(request, 'landing/landing.html', locals())
