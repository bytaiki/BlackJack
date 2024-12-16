from django.db import models


class Room(models.Model):
    chip = models.IntegerField(default = 100)

    def __str__(self):
        return f'ROOM {self.id}'

