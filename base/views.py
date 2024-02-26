from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from base.models import Task
from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema

""" CUSTOM IMPORTS"""
from base.serializers import RegisterSerializer,TaskSerializer
from base.decorators import GroupPermission
from base.pagination import TaskPagination
from base.tasks import confirmation


""" ALL TASK VIEWS WITH PAGINATION AND CUSTOM GROUP PERMISSION """
class AllTaskView(viewsets.ModelViewSet):
    permission_classes = [GroupPermission]
    pagination_class=TaskPagination
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = [
        'get'
    ]



""" LIST ALL TASK VIEW  AND ADD TASK VIEW FOR AUTHORIZED USERS ONLY"""
class TasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    CACHE_KEY_PREFIX = 'tasks'
    def get(self,request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'message':'Please provide Login Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            cached_tasks = cache.get(f'{self.CACHE_KEY_PREFIX}')

            # check if the task is already in cache
            if cached_tasks is None:
                tasks = Task.objects.filter(created_by=request.user)
                serializer =  TaskSerializer(tasks, many=True)
                cached_tasks = serializer.data
                cache.set(f'{self.CACHE_KEY_PREFIX}', cached_tasks)
                print("Data from DB before cache")
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                print("Data From CACHE")
                return Response(cached_tasks, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=TaskSerializer)
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            cache.delete(f'{self.CACHE_KEY_PREFIX}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" TASKS DETAIL VIEWS FOR AUTHORIZED USERS ONLY, GET SINGLE TASK, UPDATE TASK AND DELETE TASK VIEW"""
class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    CACHE_KEY_PREFIX = 'tasks'
    def get_object(self,pk):
        try: 
            return Task.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self,request,pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self,request,pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task,data=request.data)
        task_status = request.data['status']
        
        if serializer.is_valid():
            serializer.save()
            if task_status == 'completed':
                cache.delete(f'{self.CACHE_KEY_PREFIX}')
                confirmation.delay()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        task = self.get_object(pk)
        task.delete()
        cache.delete(f'{self.CACHE_KEY_PREFIX}')
        return Response(status=status.HTTP_204_NO_CONTENT)


""" REGISTERATION VIEW"""
class RegisterView(APIView):
    def post(self,request):
       serializer = RegisterSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response({'message':'User Account Created Successfully'})
       return Response(serializer.errors) 



"""TASK ANALYTICS VIEW, WITH CUSTOM GROUP PERMISSION """
class AnalyticsView(APIView):
    permission_classes = [GroupPermission]
    def get(self,request):
        all_tasks = Task.objects.all()
        completed_tasks_count = Task.objects.filter(status='completed').count()
        todo_tasks_count = Task.objects.filter(status='todo').count()
        in_progress_task_count = Task.objects.filter(status='in progress').count()
        
        return Response({
            'total_task_count': all_tasks.count(),
            'completed_task_count':completed_tasks_count,
            'todo_task_count':todo_tasks_count,
            'in_progress_task_count':in_progress_task_count         
        })