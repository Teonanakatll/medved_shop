from .models import ProductInBasket


def getting_basket_info(request):
    session_key = request.session.session_key
    if not session_key:  # Если нет ключа сессии создаём
        # vorkaround for never Django versions
        request.session["session_key"] = 123
        # re-apply value
        request.session.cycle_key()

    # Выбираем queryset по ключу сессии
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()

    return locals()
