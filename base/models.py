from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    module_choices = (
        (0, "On-Progress"),
        (1, "Not Completed"),
        (2, "Completed"),
    )
    complete = models.CharField(max_length=10, choices=module_choices, default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    task_name = models.ForeignKey('TaskName', models.CASCADE, null=True, blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'


class TaskName(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


