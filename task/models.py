from django.db import models
from column.models import ColumnModel

class TaskModel(models.Model):
    task = models.CharField(blank=False, null=False)
    column = models.ForeignKey(ColumnModel, blank=False, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('task', 'column')
    

    def __str__(self):
        return f'{self.id}'