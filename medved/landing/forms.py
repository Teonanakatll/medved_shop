from django.forms import ModelForm, TextInput, EmailInput
from .models import Subscriber

class SubscriberForm(ModelForm):

    class Meta:
        model = Subscriber
        # Поля которые нужно добавить в форму
        # fields = ["email", "name"]
        # Поля которые нужно исключить из формы
        exclude = [""]

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email '
            })
        }