from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDeleteView, \
    CustomLoginView, RegisterPage, TaskReorder, \
    TaskNameList, TaskNameReorder, TaskNameCreate, TaskNameUpdate, TaskNameDeleteView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('task_list/<int:pk>/', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/<int:pk>/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    # my urls,
    path('', TaskNameList.as_view(), name='task-name'),
    path('taskname-reorder/', TaskNameReorder.as_view(), name='taskname-reorder'),
    path('taskname-create/', TaskNameCreate.as_view(), name='taskname-create'),
    path('taskname-update/<int:pk>/', TaskNameUpdate.as_view(), name='taskname-update'),
    path('taskname-delete/<int:pk>/', TaskNameDeleteView.as_view(), name='taskname-delete'),

]
