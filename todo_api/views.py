from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Todo
from .serializers import TodoSerializer

class TodoListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, *args , **kwargs):
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos , many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args , **kwargs):
        
        data = {
            'task' : request.data.get('task'),
            'completed' : request.data.get('completed'),
            'user' : request.user.id
        }

        serializer = TodoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, todo_id, *arg, **kwargs):

        todo_instance = self.get_object(todo_id, request.user.id)
        
        if not todo_instance:
            return Response(
                {"res": "Object with the given todo id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id = todo_id, user = user_id)
        except:
            return None

    def put(self, request, todo_id, *arg, **kwargs):
       
        todo_instance = self.get_object(todo_id, request.user.id)
        
        if not todo_instance:
            return Response(
                {"res": "Object with the given todo id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )

        data = {
            'task' : request.data.get('task'),
            'completed': request.data.get('completed'),
            'user' : request.user.id
        }

        serializer = TodoSerializer(instance = todo_instance, data = data, partial = True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id, *arg, **kwargs):
        
        todo_instance = self.get_object(todo_id, request.user.id)
        
        if not todo_instance:
            return Response(
                {"res": "Object with the given todo id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )

        todo_instance.delete()

        return Response(
            {"res": "todo instance has been successfully deleted"},
            status = status.HTTP_200_OK
        )       

