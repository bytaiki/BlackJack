from django import forms
from .models import CustomUser

class BetForm(forms.Form):
    bet = forms.IntegerField(label='ベット額', min_value=1)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_bet(self):
        bet = self.cleaned_data['bet']
        if self.user and bet > self.user.chip:
            raise forms.ValidationError("正しい値を入力してください")
        return bet
