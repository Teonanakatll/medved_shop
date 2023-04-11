from django.http import JsonResponse
from django.shortcuts import render
from .models import ProductInBasket


def basket_adding(request):
    return_dict = dict()

    # Сохраняем в переменной ключ сессии
    session_key = request.session.session_key
    print(request.POST)

    # Присваиваем переменной data request.POST и вытаскиваем из него данные
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")

    # Сохраняем новый продукт в корзине
    new_product = ProductInBasket.objects.create(session_key=session_key, product_id=product_id, nmb=nmb)

    # По session_key считываем общее количество данного товара
    products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    # Передаём в словарь return_dict количество
    return_dict["products_total_nmb"] = products_total_nmb

    return JsonResponse(return_dict)
