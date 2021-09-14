import json
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import TodoList


class TodoTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='shivam', password='admin123')
        self.token = Token.objects.create(user=self.user)

        data = {
            "title": "testing 8",
            "content": "Complete the assignment by tonight",
            "due_date": "2021-09-14",
            "user_id": self.user.id
        }

        self.todo_list = TodoList.objects.create(**data)

    def test_todocreation(self):

        data = {
            "title": "testing 8",
            "content": "Complete the assignment by tonight",
            "due_date": "2021-09-14",
            "user": self.user.id
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))
        response = self.client.post(reverse('create-todo-task'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todocreation_wrong_userId(self):

        data = {
            "title": "testing 8",
            "content": "Complete the assignment by tonight",
            "due_date": "2021-09-14",
            "user": 2
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))
        response = self.client.post(reverse('create-todo-task'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_todo_list(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))
        response = self.client.get(reverse('get-todo-task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_todo_task(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))
        response = self.client.get(reverse('get-todo-task', kwargs={'task_id': self.todo_list.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_task(self):

        data = {
            "title": "testing 9",
            "content": "Complete the assignment by tonight",
            "due_date": "2021-09-15",
            "user": self.user.id
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))
        response = self.client.post(reverse('update-todo-task', kwargs={'task_id': self.todo_list.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
