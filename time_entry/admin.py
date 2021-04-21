from django.contrib import admin

# Register your models here.
from time_entry.models import TaskModel

admin.site.register(TaskModel)