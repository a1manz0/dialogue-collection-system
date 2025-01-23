from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import ClientQuestion
from .forms import ClientQuestionForm
import json
import csv
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

class QuestionListView(LoginRequiredMixin, ListView):
    model = ClientQuestion
    template_name = 'dialogues_app/question_list.html'
    context_object_name = 'questions'
    paginate_by = 10

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = ClientQuestion
    form_class = ClientQuestionForm
    template_name = 'dialogues_app/question_form.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientQuestion
    form_class = ClientQuestionForm
    template_name = 'dialogues_app/question_form.html'
    success_url = reverse_lazy('question_list')

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = ClientQuestion
    template_name = 'dialogues_app/question_confirm_delete.html'
    success_url = reverse_lazy('question_list')

@login_required
def export_json(request):
    questions = ClientQuestion.objects.all()
    data = []
    
    for question in questions:
        data.append({
            'topic': question.get_topic_display(),
            'requires_crm': question.requires_crm,
            'dialogue': question.dialogue_example,
            'created_by': question.created_by.username,
            'created_at': question.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    response = HttpResponse(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="dialogues.json"'
    return response

@login_required
def export_csv(request):
    questions = ClientQuestion.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dialogues.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Тема', 'Требуется CRM', 'Диалог', 'Создал', 'Дата создания'])
    
    for question in questions:
        writer.writerow([
            question.get_topic_display(),
            'Да' if question.requires_crm else 'Нет',
            question.dialogue_example,
            question.created_by.username,
            question.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response