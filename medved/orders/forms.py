from django import forms


class CheckoutContactForm(forms.Form):
    # Атрибут required добавляется обязательным полям формы. Если поле с таким атрибутом не заполнено,
    # то при отправке формы браузер покажет предупреждение и отменит отправку.
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)