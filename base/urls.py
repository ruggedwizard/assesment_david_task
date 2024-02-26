from django.urls import path, include
from base import views
from rest_framework.routers import DefaultRouter

# Define Router
router = DefaultRouter()
router.register('all-task',views.AllTaskView)

urlpatterns = [
    path('tasks/',views.TasksView.as_view()),
    path('task/<str:pk>/',views.TaskDetailView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('',include(router.urls)),
    path('analytics/', views.AnalyticsView.as_view())
]