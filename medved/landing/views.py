from django.shortcuts import render
from .forms import SubscriberForm

def landing(request):
    name = "Syava"
    current_day = "05.03.1998"
    form = SubscriberForm(request.POST or None)
    error = ''
    # Если форма на странице заполненна и прошла валидацию
    if request.method == "POST" and form.is_valid():
        # Вывести POST-запрос
        print(request.POST)
        # Вывести очищенные данные
        print(form.cleaned_data)
        data = form.cleaned_data  # Присваиваем пер. data словарь cleaned_data
        print(data["name"])       # Выводим поле name
        form.save()        # Сохраняем форму
    else:
        error = "Ошибка заполнения формы"
    return render(request, 'landing/landing.html', locals())
