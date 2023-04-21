from .models import ProductInBasket

# Данные выводим в navbar
def getting_basket_info(request):
    """ Формирует список товаров для отображения в корзине. """
    session_key = request.session.session_key
    if not session_key:  # Если нет ключа сессии создаём
        # vorkaround for never Django versions
        request.session["session_key"] = 123
        # re-apply value
        request.session.cycle_key()

    # Выбираем queryset по ключу сессии, которые ещё не добавлены в заказ (order__isnull=True).
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()

    return locals()
