// Инициируем обёртку jquery после загрузки html-документа
$(document).ready(function(){
    // Создаём переменную,
    // $ значит к этому элементу страницы абращаемся как к элементу jquery
    // # выбираем элемент по id
    var form = $('#form_buying_product');
    // Выводим переменную в консоль
    console.log(form);
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

            // В переменной дата будут данные которые мы отправляем
            var data = {};
            data.product_id = product_id;
            data.nmb = nmb;

            // В переменной csrf_token добавляем токен который нужен джанго чтобы делать post-запросы
            var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;
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
                    if (data.products_total_nmb){
                        $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                    }
                },
                error: function(){
                    console.log("error")
                }
            })

        // Обращаемся к елементу на уровень ниже (ul)
        // И с помощю функции append() добавляем в него элемент
        $('.basket-items ul').append('<li>'+product_name+', '+ nmb + 'шт. ' + 'по ' + product_price + 'р  ' +
        // Чтоб появился курсор добавляем href=""
        '<a class="delete-item" href="">   x</a>'+
        '</li>');

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
    // Чтобы удалить из корзины товар через класс delete-item который был созданн
    // после дабавления товара, необходимо снова обратиться через $(document)
    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        // Выбираем этот же елемент через (this), и выбираем ближайший к нему элемент li
        $(this).closest('li').remove();
    })
});