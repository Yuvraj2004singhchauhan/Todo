from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'due_date', 'completed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['title', 'priority', 'due_date']:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
            })

        self.fields['due_date'].widget.attrs.update({
            'type': 'date'
        })

        self.fields['completed'].widget.attrs.update({
            'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500'
        })