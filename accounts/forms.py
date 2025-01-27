from django.contrib.auth.forms import UserCreationForm
from bj.models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', )