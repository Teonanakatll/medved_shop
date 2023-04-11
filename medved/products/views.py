from django.shortcuts import render
from .models import Product


def product(request, product_id):

    product = Product.objects.get(id=product_id)

    # Django session : https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Sessions
    # Достаём ключ сессии
    session_key = request.session.session_key
    # Если пользователь не авторизован, создаём ключ вручную с помощю cycle_key()
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)
    print(session_key)

    return render(request, 'products/product.html', locals())
