from django.db import models
from django.utils import timezone
from common.mixins import CreatedAndUpdatedMixin
from django.contrib.auth.models import User


class TodoList(CreatedAndUpdatedMixin):  #Todolist able name that inherits models.Model
    title = models.CharField(max_length=250)  # a varchar
    content = models.TextField(null=True, blank=True)  # a text field 
    due_date = models.DateField(null=True, blank=True)  # a date
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_on"]  #ordering by the created field

    def __str__(self):
        return self.title  #name to be shown when called
