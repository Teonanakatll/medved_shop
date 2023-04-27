# -*- coding: utf-8 -*-
from emails.models import EmailSendingFact
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

from medved.settings import FROM_EMAIL, EMAIL_ADMIN
from django.forms.models import model_to_dict

class SendingEmail(object):
    # Адрес отправителя
    from_email = "BestShopEver <%s>" % FROM_EMAIL
    # Ответить отправителю (или подставить другой имейл)
    reply_to_emails = [from_email]
    target_emails = []
    # Cc: (копия, carbon copy) — вторичные получатели письма, которым направляется копия.
    # Они видят и знают о наличии друг друга.
    # Bcc: (скрытая копия, blind carbon copy) — скрытые получатели письма,
    # чьи адреса не показываются другим получателям.
    bcc_emails = []

    def sending_email(self, type_id, email=None, order=None):

        # Если нет поля email, значти type_id==1 и письмо отправляется администратору
        if not email:
            email = EMAIL_ADMIN

        # Имейл получателя
        self.target_emails = [email]

        vars = dict()

        if type_id == 1:  # Получатель админ
            subject = "Новый заказ"
            # model_to_dict() - Возвращает словарь с полями и их зночениями, из переданной модели, field: value
            vars["order_field"] = model_to_dict(order)  # model_to_dict(instance, fields=[], exclude=[])
            vars["order"] = order
            # order.productinorder_set - выбирает все обьекты productinorder, которые через ForeignKey
            # ссылаются на данный экземпляр класса order
            vars["products_in_order"] = order.productinorder_set.filter(is_activ=True)

            # get_template() загружает шаблон из загрузчика. Если настроен загрузчик,
            # то этот метод запрашивает у загрузчика шаблон и возвращает шаблон.
            # Ищет в по тем путям, которые прописаны в TEMPLATES["DIRS"] шаблон,
            # имя которого передаётся в эту функцию, и возвращает объект Template.

            # Когда у вас есть скомпилированный Templateобъект, вы можете визуализировать контекст с ним. Вы можете
            # повторно использовать один и тот же шаблон, чтобы отображать его несколько раз в разных контекстах.
            # Конструктор django.template.Contextпринимает необязательный аргумент — словарь,
            # отображающий имена переменных в значения переменных.
            # Template.render( контекст )
            message = get_template('emails_templates/order_notification_admin.html').render(vars)

        elif type_id == 2:  # Получатель пользователь
            subject = 'Ваш заказ в магазине "Наш магазин" получен!'
            message = get_template('emails_templates/order_notification_customer.html').render(vars)

        # Центральным классом в пакете email является класс EmailMessage, импортированный из модуля email.message.Это
        # базовый класс для объектной модели email. EmailMessage предоставляет основные функции для настройки и  запроса
        # полей заголовков, для доступа к телу сообщения, а также для создания или изменения структурированных сообщений
        msg = EmailMessage(
                subject, message, from_email=self.from_email, to=self.target_emails,
                bcc=self.bcc_emails, reply_to=self.reply_to_emails
                )
        # Возвращает тип подсодержимого сообщения. Это часть subtype строки, возвращаемой get_content_type().
        # Возвращает тип содержимого сообщения, приведённый к нижнему регистру формы maintype/subtype.
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()

        kwargs = {
            "type_id": type_id,
            "email": email,
        }
        # Если есть заказ то передаём его в словарь kwargs
        if order:
            kwargs["order"] = order
        EmailSendingFact.objects.create(**kwargs)

        print('Email was successfully!')
