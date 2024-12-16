from django import forms
from .models import Room


class BetForm(forms.Form):
    bet = forms.IntegerField(label='ベット額',min_value=1)

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)

    def clean_bet(self):
        bet = self.cleaned_data['bet']
        if self.room and bet > self.room.chip:
            raise forms.ValidationError("正しい値を入力してください")
        return bet

