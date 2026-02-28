from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from .models import Task
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .forms import TaskForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            })

class ToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        return redirect('home')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
    paginate_by = 8

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        search_query = self.request.GET.get('search')
        filter_value = self.request.GET.get('filter')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if filter_value == 'completed':
            queryset = queryset.filter(completed=True)
        elif filter_value == 'pending':
            queryset = queryset.filter(completed=False)
        sort_by = self.request.GET.get('sort')

        if sort_by == 'due':
            queryset = queryset.order_by('due_date')
        elif sort_by == 'priority':
            queryset = queryset.order_by('priority')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tasks = Task.objects.filter(user=self.request.user)

        context['total_tasks'] = user_tasks.count()
        context['completed_tasks'] = user_tasks.filter(completed=True).count()
        context['pending_tasks'] = user_tasks.filter(completed=False).count()

        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Task Updated successfully!")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "Task deleted successfully!")
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
