from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

from time_entry import views

urlpatterns = [

    path('', views.Login.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('task/', views.Task.as_view(), name="task"),
    path('js/', TemplateView.as_view(template_name='time_entry/dashboard.html')),
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path('list/', views.TaskListView.as_view(), name='list'),
    path('list/<int:pk>', views.TaskDetailView.as_view(), name='detail')
]
