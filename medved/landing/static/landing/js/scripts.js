// Инициируем обёртку jquery после загрузки html-документа
$(document).ready(function(){
    // Создаём переменную,
    // $ значит к этому элементу страницы абращаемся как к элементу jquery
    // # выбираем элемент по id
    var form = $('#form_buying_product');
    // Выводим переменную в консоль
    console.log(form);

    // Передаём в функцию атрибуты product_id, nmb и is_delete - для удаления товара
    function basketUpdating(product_id, nmb, is_delete){
            // В переменной дата будут данные которые мы отправляем
            var data = {};
            data.product_id = product_id;
            data.nmb = nmb;

            // В переменной csrf_token добавляем токен который нужен джанго чтобы делать post-запросы
            var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;

            console.log(data["is_delete"])
            // Из за разного написания True в ждава и питоне уточняем
            if (is_delete){
                data["is_delete"] = true;
                console.log(data["is_delete"]);
            }

            // Адресс на который необходимо отправлять post-запрос
            // Считываем url с атрибута action формы
            var url = form.attr("action");

            console.log(data)

            $.ajax({
                url: url,
                type: 'POST',
                data: data,  // Переменная с данными
                cache: true,
                success: function (data) {  // При успешном ответе сервера вызывается функция
                    console.log("OK");
                    // Выводим в консоль данные полученные из orders/views.py
                    console.log(data.products_total_nmb);
                    // Если есть значение total (количество позиций товара в корзине за сессию) то вписываем его рядом с корзиной
                    // или значение равно нулю, выполняем этот код
                    if (data.products_total_nmb || data.products_total_nmb == 0){
                        $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                        // Выводим данные из JsonResponse
                        console.log(data.products);
                        // Очищаем элемент ul с помощю метода .html("")
                        $('.basket-items ul').html("");
                        // Через цикл выводим записи товаров в корзину, k - индекс, v - сам обьект
                        $.each(data.products, function(k, v){
                            // Обращаемся к елементу на уровень ниже (ul)
                            // И с помощю функции append() добавляем в него элемент
                            $('.basket-items ul').append('<li>'+v.name+', '+ v.nmb + 'шт. ' + 'по ' + v.price_per_item + 'р  ' +
                            // Чтоб появился курсор добавляем href=""
                            // Добавляем дата-аттрибут data-product_id для возм. удаления
                             '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>'+
                            '</li>');

                        })
                    }
                },
                error: function(){
                    console.log("error")
                }
            })

    }

    // Присоединяем к форме событие, при событии передаём функции параметр е (event) - cтандартвый
    // евент отправки формы
    form.on('submit', function(e){
        // прмменяем к е функцмю preverntDefault(), которая отменяет стандартное поведение
        // евента (чтобы форма не отправлялась)
        e.preventDefault();
        console.log('123');
        // Создаём переменную nmb
        // По id вызываем элемент input формы и с помощю .val() берем его значение
        var nmb = $('#num').val();
        console.log(nmb);
        // Создаём переменную с id кнопки
        var button_sub = $('#button-submit');
        // Обращаемся к переменной кнопки и с помощью ф. .data() берем data атрибуты и
        // присваиваем их значения переменным
        var product_id = button_sub.data('product_id');
        var product_name = button_sub.data('product_name');
        var product_price = button_sub.data('product_price')
        console.log(product_id);
        console.log(product_name);
        console.log(product_price);

        // Берем значения из кода выше
        basketUpdating(product_id, nmb, is_delete=false)

        // получить значение атрибута data у первого элемента текущего набора
        //$('селектор').attr('data-*');
        var f = $('#button-submit').attr('data-fuck')
        console.log(f)

        // добавить или изменить значение атрибута data у всех выбранных элементов
        //$('селектор').attr('data-*','значение');

    })

    // Написание функции (дублирование кода)
    function showingBasket(){
        // .toggleClass - добавляет или убирает класс
        $('.basket-items').removeClass('visually-hidden');
    }


    // По клику  на .basket-container
    $('.basket-container').on('click', function(e){
        e.preventDefault();
        showingBasket()
    });
    // По наведению мыши
    $('.basket-container').mouseover(function(){
        showingBasket()
    });
    // При отводе мыши
    $('.basket-container').mouseout(function(){
        // $('.basket-items').addClass('visually-hidden');
        showingBasket()
    });
    // По клику на крестик
    // Чтобы удалить из корзины товар через класс delete-item который был созданн
    // после дабавления товара, необходимо снова обратиться через $(document)
    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        // Считываем значение id с дата атрибута кнопки
        product_id = $(this).data("product_id");
        nmb = 0;
        // Вызываем функцию basketUpdating с параметром true для удаления товара
        basketUpdating(product_id, nmb, is_delete=true);
        // Выбираем этот же елемент через (this), и выбираем ближайший к нему элемент li
        $(this).closest('li').remove();
    });

    // Функция расчитывает общую стоимость товаров в корзине
    function calculatingBasketAmount(){
        // Проверяем вызывается ли функция
        console.log("calculatingBasketAmount");
        // Переменная для расчёта и вывода суммы в id=total_order_amount
        var total_order_amount = 0;
        // Проходим циклом по каждому значению (span class=...) в списке товаров на checkout.html
        $('.total-product-in-basket-amount').each(function(){
            // Переводим str в int с помощю функции parseInt(), или в float через parseFloat() и .toFixed(2)
            total_order_amount += parseFloat($(this).text());
        });
        // Вписываем результат в span id="total_order_amount"
        $('#total-order-amount').text(total_order_amount.toFixed(2));
    };

    // Функция отслеживает изменения в инпуте (span class="product-in-basket-nmb")
    $(document).on('change', ".product-in-basket-nmb", function(){
        console.log("product-in-basket-nmb");
        // Считываем текущее количество с инпута
        var current_nmb = $(this).val();
        // Считываем значение с ближайшей ячейки tr к нашей (в которой меняем кол-во)
        var current_tr = $(this).closest("tr");
        // Считываем стоимость товара cо span class="product-price", переводим в float
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        // Находим общую стоимость позиции товара, переводим в float
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        // Находим текущий span class="total_product_in_basket_amount" и вписываем значение
        console.log(total_amount);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);
        // Вызываем функцию calculatingBasketAmount() для подсчёта общего кол-ва
        calculatingBasketAmount();
    });

    calculatingBasketAmount();

});