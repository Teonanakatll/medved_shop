from django import forms
from .models import Subscribers

class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscribers
        # Поля которые нужно добавить в форму
        # fields = ["email", "name"]
        # Поля которые нужно исключить из формы
        exclude = [""]