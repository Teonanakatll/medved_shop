from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from .models import ProductInBasket, ProductInOrder, Order
from .forms import CheckoutContactForm
from django.contrib.auth.models import User


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
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, is_active=True, product_id=product_id, defaults={"nmb": nmb})  # defaults={поля по умолчанию}

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

def checkout(request):
    session_key = request.session.session_key
    # Выбираем товары в корзине по ключу сессии исключая продукты которые уже есть в заказе.
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        # Если форма прошла валидацию создаём юзера
        if form.is_valid():
            print("yes")
            data = request.POST
            # Если поле пустое чтоб не было исключения пишем через get()
            name = data.get("name", "one")  # "one" - любое значение по умолчанию
            phone = data["phone"]
            # Выбираем или создаём юзера, устанавливаем телефон как имя юзера
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            # Создаём заказ с данными юзера, устанавливаем статус
            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)
            # Считываем товары из POST запроса
            for name, value in data.items():
                # Если имя элемента словаря начинается с ("...")
                if name.startswith("product_in_basket_"):
                    # Берем последний элемент списка
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    # Считываем обьект по id
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    # Возникла ошибка can't multiply sequence by non-int of type 'decimal.Decimal'
                    # проверяем значение поля value
                    print(type(value))
                    # Устанавливаем количество товара со страницы checkout.html (при изменении)
                    product_in_basket.nmb = value
                    # Указываем заказ к которому относится товар
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    # Создаём продукт в заказе
                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)

        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())

def admin_orders(request):
    # Второй уровень проверки что текущий пользователь это суперюзер. if user.is_superuser тогда выполняем
    # весь код. Если нет-то return HttpResponseRedirect(reverce("home")
    user = request.user

    # Выбираем все существующие заказы и добавляем им поле 'products_nmb' котораму присваиваем
    # значение количество связанных наименований товаров связанных с каждым заказом
    # values() - предостовляет данные в виде словоря (a не queryset), предоставляет записи только из текущей модели
    # если необходимы записи из связанных моделей или их полей то нужно перечислить их в скобках ("...", "...")
    orders = Order.objects.annotate(products_nmb=Count('productinorder')).values()
    # Присваиваем переменной список со всеми id заказов
    order_ids = [order["id"] for order in orders]

    # Формируем список активных ProductInOrder, id товаров в которых находится в списке order_ids
    # выбираем только поля в .values()
    products_in_order = ProductInOrder.objects.filter(is_activ=True, order_id__in=order_ids)\
        .values("order_id", "product__name", "nmb", "price_per_item", "total_price")

    # merging_dicts(orders (список словарей), products_in_order (список славарей), id, order_id)
    def merging_dicts(l1, l2, key1, key2):
        merged = {}
        # print(l1)
        # print(len(l1))
        # Для каждого словаря в списке заказав
        for item in l1:
            # print(item[key1])
            # Выбираем из каждого словаря элемент по ключу order["id"] - тоесть выбираем значение id заказа
            # Добавляем в merged словарь: {"id заказа": {словарь заказа}}, выносим id как ключ словаря
            merged[item[key1]] = item
        # Для каждого словаря в списке product_in_order
        for item in l2:
            try:
                # Берем значение по ключу "order_id" и используя его зночение как ключ для созданного словаря
                # merged, проверяем существует ли в связанном славаре ключ "products".
                if "products" in merged[item[key2]]:
                    # Если существует то добавляем, к значению этого ключа (в список) текущий товар
                    merged[item[key2]]["products"].append(item)
                else:
                    # Если не существует то создаём в заказе словарь {products:[текущий продукт]} со списком
                    # в который будем добавлять связанные товары
                    merged[item[key2]]["products"] = [item]
            except Exception as e:
                return True

        # Проходим циклом по словарю merged и создаём список с его зночениями, в итоге получаем список заказов
        # в каждом из которых есть словарь "products" со списком связанных товаров

        orders = [val for (_, val) in merged.items()]
        return orders

    orders = merging_dicts(list(orders), list(products_in_order), "id", "order_id")
    return render(request, 'orders/admin_orders.html', locals())
