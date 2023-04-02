from django.shortcuts import render
from .forms import SubscriberForm
from products.models import Product, ProductImage


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

def home(request):
    products_images = ProductImage.objects.filter(is_activ=True, is_main=True, product__is_activ=True)
    # Обращение в queryset к связанным полям
    products_images_phones = products_images.filter(product__category_id=1)
    products_images_laptops = products_images.filter(product__category_id=2)
    return render(request, 'landing/home.html', locals())