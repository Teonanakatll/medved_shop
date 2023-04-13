from django.http import JsonResponse
from django.shortcuts import render
from .models import ProductInBasket


def basket_adding(request):
    return_dict = dict()
                                     # ДАННЫЕ ПОЛУЧАЕМ ОТ ФРОНТЕНДА
    # Сохраняем в переменной ключ сессии
    session_key = request.session.session_key
    print(request.POST)

    # Присваиваем переменной data request.POST и вытаскиваем из него данные
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")

    # Получаем ат фронтенда данные переменной is_delete
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        # Возвращает обьект (ищет по совпадающим полям), или создаёт со всеми указанными полями
        # Метод возвращает добавленный обьект и буллевое значение (created) True если дабавление прошло успешно
        # Если обьектов больше одного вернет MultipleObjectsReturned
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, is_active=True,
                                                                     product_id=product_id, defaults={"nmb": nmb})  # defaults={поля по умолчанию}

        # Если поле уже существует обновляем количество
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)  # Сохраняем изменения количества в базе данных

    # common code for 2 cases
    # По session_key считываем общее количество данного товара (queryset)
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    # Передаём в словарь return_dict количество
    return_dict["products_total_nmb"] = products_total_nmb

    # Создаём список для передачи товаров в фронтенд (Ajax)
    return_dict["products"] = list()
    for item in products_in_basket:
        product_dict = dict()  # Создаём словарь для кождого товара
        # id для передачи в Ajax для удаления товара
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)  # Добавляем словорь в список

    # Передаём в Ajax
    return JsonResponse(return_dict)
