from django.db import models


class Room(models.Model):
    chip = models.IntegerField(default = 100)

    def __str__(self):
        return f'ROOM {self.id}'

class GameResult(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    bet_result = models.IntegerField()
    p_hand_sum = models.PositiveIntegerField()
    d_hand_sum = models.PositiveIntegerField()
    p_hand_img = models.CharField(max_length=200)
    d_hand_img = models.CharField(max_length=200)
    played_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Game{self.id} at Room{self.room.id}'

