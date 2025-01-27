from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    chip = models.IntegerField(default=100)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class GameResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    bet_result = models.IntegerField()
    p_hand_sum = models.PositiveIntegerField()
    d_hand_sum = models.PositiveIntegerField()
    p_hand_img = models.CharField(max_length=200)
    d_hand_img = models.CharField(max_length=200)
    played_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Game{self.id} at {self.user.username}'

