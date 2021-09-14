from django.conf.urls import url
from . import views as Views


urlpatterns = [
    url('get-task-list/$', Views.GetTodotaskList.as_view(), name='get-todo-task-list'),
    url('get-task/(?P<task_id>[0-9]+)/$', Views.GetTodotask.as_view(), name='get-todo-task'),
    url('update-task/(?P<task_id>[0-9]+)/$', Views.UpdateTodotask.as_view(), name='update-todo-task'),
    url('create-task/$', Views.CreateTodoTask.as_view(), name='create-todo-task'),
    url('delete-task/(?P<task_id>[0-9]+)/$', Views.DeleteTodoTask.as_view(), name='delete-todo-task')
]
