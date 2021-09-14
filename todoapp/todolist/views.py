import logging
from todoapp.settings import DEBUG
import traceback
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TodoList
from .serializers import TodoListSerializer

from .utils import set_redis, get_redis

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GetTodotaskList(APIView):
    permissions = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        todo_list = TodoList.objects.filter(user=user)
        serializer = TodoListSerializer(todo_list, many = True)
        logger.info('GetTodotaskList: sending response {}'.format(serializer.data))
        return Response(serializer.data)


class GetTodotask(APIView):
    permissions = (IsAuthenticated,)

    def authorised(self, user_id, user):
        if user_id != user.id:
            return False
        return True

    def get(self, request, task_id):
        user = request.user

        key = 'task:{}'.format(task_id)
        status, val = get_redis(key)

        if not val:

            todo_list = TodoList.objects.filter(id=task_id).first()

            if not todo_list:
                logger.info('GetTodotask: No todo task for the user')
                return Response({
                    'message': 'No Task found'
                }, status=404)

            user_id = todo_list.user_id
            if not self.authorised(user_id, user):
                logger.error('GetTodotask: User did not match')
                return Response({
                    'message': 'Not allowed to view this task'
                }, status=403)

            serializer = TodoListSerializer(todo_list)
            logger.info('GetTodotask: sending response {}'.format(serializer.data))
            return Response(serializer.data)

        user_id = val.get('user')
        if not self.authorised(user_id, user):
            logger.error('GetTodotask: Not allowed to view this task')
            return Response({
                'message': 'Not allowed to view this task'
            }, status=403)

        return Response(val, status=200)


class UpdateTodotask(APIView):
    permissions = (IsAuthenticated,)

    def post(self, request, task_id):
        try:
            task = TodoList.objects.get(id=task_id)
            serializer = TodoListSerializer(instance=task, data=request.data)
            if serializer.is_valid():
                serializer.save()

                data = serializer.data
                _id = data.get('id')
                key = 'task:{}'.format(_id)
                status, res = set_redis(key, data)

                logger.info('UpdateTodotask: serializer.data')
                return Response(serializer.data)

            logger.error('UpdateTodotask: {}'.format(serializer.errors))
            return Response({
                'reason': serializer.errors
            },status=406)    

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response({
                'message': 'No task with this Id'
            }, status=404)


class CreateTodoTask(APIView):
    permissions = (IsAuthenticated,)

    def post(self, request):

        user = request.user
        user_id = request.data.get('user')

        if user_id:
            user_id = int(user_id)

        if user.id != user_id:
            return Response({
                "message": ['User not allowed to create this todo task']
            }, status=403)

        serializer = TodoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            data = serializer.data
            _id = data.get('id')
            key = 'task:{}'.format(_id)
            status, res = set_redis(key, data)

            return Response(serializer.data)

        logger.error('CreateTodoTask: {}'.format(serializer.errors))
        return Response({
            'message': serializer.errors
        },status=406)


class DeleteTodoTask(APIView):
    permissions = (IsAuthenticated, )

    def delete(self, request, task_id):
        task = TodoList.objects.filter(id=task_id).first()
        if not task:
            logger.error('DeleteTodoTask: No task found')
            return Response({
                'message': 'No task found'
            }, status=404)

        if task.user_id != request.user.id:
            logger.error('DeleteTodoTask: not allowed to delete this task')
            return Response({
                'message': 'not allowed to delete this task'
            }, status=403)

        task.delete()
        logger.info('DeleteTodoTask: succesfully deleted task')
        return Response({
            'message': 'succesfully deleted task'
        }, status=200)
