from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        # Поля которые нужно добавить в форму
        # fields = ["email", "name"]
        # Поля которые нужно исключить из формы
        exclude = [""]