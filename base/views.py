from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task, TaskName
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-name')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskNameList(LoginRequiredMixin, ListView):
    model = TaskName
    context_object_name = 'taskname'


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    task_name_context = TaskName.objects.all()

    def get_context_data(self, **kwargs):
        p = self.request
        task_name_id = TaskName.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['task_name_context'] = task_name_id
        context['tasks'] = context['tasks'].filter(user=self.request.user, task_name=self.kwargs['pk'])
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'task_name']
    success_url = reverse_lazy('task-name')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task_name = TaskName.objects.get(pk=self.kwargs.get('pk'))
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

# **************************     my changes    **************************


class TaskNameReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('task-name'))


class TaskNameCreate(LoginRequiredMixin, CreateView):
    model = TaskName
    fields = ['name']
    success_url = reverse_lazy('task-name')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskNameCreate, self).form_valid(form)


class TaskNameUpdate(LoginRequiredMixin, UpdateView):
    model = TaskName
    fields = ['name']
    success_url = reverse_lazy('task-name')