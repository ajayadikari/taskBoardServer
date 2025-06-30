from django.db import models
from board.models import BoardModel

STATUS = (
    ('t', 'To Do'), 
    ('i', 'In Progress'), 
    ('d', 'Done'),
)

class ColumnModel(models.Model):
    board = models.ForeignKey(BoardModel, null=False, blank=False, on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS, max_length=1, default='t')


    def __str__(self):
        return f"{self.board}-{self.status}"