from django.contrib.auth.models import User
from django.db import models


class TaskModel(models.Model):
    Project_1 = 'Project 1'
    Project_2 = 'Project 2'
    Project_3 = 'Project 2'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    project_CHOICES = [
        (Project_1, 'Project 1'),
        (Project_2, 'Project 2'),
        (Project_3, 'Project 3'),

    ]
    project = models.CharField(
        max_length=10,
        choices=project_CHOICES,
        default=Project_3,
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.task_name
