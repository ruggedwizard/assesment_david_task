from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group


"""CUSTIOM IMPORTS"""
from base.models import Task


class TestModelTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        """ Create groups for testing"""
        self.admin_group = Group.objects.create(name='admin')
        self.regular_user_group = Group.objects.create(name='regular_users')
        self.other_user = Group.objects.create(name='others')

        """ Create a user with the admin access group"""
        self.admin_user = User.objects.create_user(username='adminuser',password='adminpassword')
        self.admin_user.groups.add(self.admin_group)
        self.admin_refresh = RefreshToken.for_user(self.admin_user)
        self.admin_access = self.admin_refresh.access_token

        """ create a user with the regular users access group"""
        self.regular_user = User.objects.create_user(username='regular_user',password='regularuserpassword')
        self.regular_user.groups.add(self.regular_user_group)
        self.regular_refresh = RefreshToken.for_user(self.regular_user)
        self.regular_access = self.regular_refresh.access_token


        """create some dummy data for testing"""
        self.task1 = Task.objects.create(
            title = 'Simple Task 1',
            description = 'This is a simple task description', 
            created_by = self.admin_user
        )
        self.task2 = Task.objects.create(
            title = 'Simple Task 2',
            description = 'This is another simple task',
            status = 'in progress',
            created_by = self.regular_user
        )

        
    """Test to count the number of tasks in the database"""
    def test_task_model_exists(self):
        tasks = Task.objects.count()
        self.assertEqual(tasks,2)
    
    """Test admin user group can access all task with pagination"""
    def test_admin_user_group_list_all_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ str(self.admin_access))
        response = self.client.get('/all-task/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),4)
    
    
    """ Test regular user group cannot access all task with pagination""" 
    def test_regular_user_group_cannot_list_all_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION ='Bearer '+ str(self.regular_access))
        response = self.client.get('/all-task/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    """test users can create task"""
    def test_users_can_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+ str(self.regular_access))
        data = {'title':'test task', 'description': 'test task description'}
        response = self.client.post('/tasks/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

