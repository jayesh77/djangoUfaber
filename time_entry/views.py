from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView
from time_entry.forms import UserForm
from time_entry.models import TaskModel


class Login(LoginView):
    template_name = 'time_entry/login.html'


class SignUp(CreateView):
    form_class = UserForm
    template_name = 'time_entry/signup.html'
    success_url = '/list/'

    def form_valid(self, form):
        form.save()
        username, password = form.cleaned_data['username'], form.cleaned_data['password1']
        valid = super(SignUp, self).form_valid(form)
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


@method_decorator(login_required(login_url='login'), name='dispatch')
class Task(CreateView):
    model = TaskModel
    fields = ['task_name', 'project', 'start_time', 'end_time']
    template_name = 'time_entry/task.html'
    success_url = '/list/'

    def get_form(self, form_class=None):
        form = super(Task, self).get_form()
        form.fields['start_time'].widget = AdminTimeWidget()
        form.fields['end_time'].widget = AdminTimeWidget()
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class TaskListView(ListView):
    model = TaskModel

    def get_queryset(self):
        return super(TaskListView, self).get_queryset().filter(user=self.request.user)


@method_decorator(login_required(login_url='login'), name='dispatch')
class TaskDetailView(DetailView):
    model = TaskModel

    def get_object(self, queryset=None):
        obj = super(TaskDetailView, self).get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404()
        return obj
