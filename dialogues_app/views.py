from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import ClientQuestion
from .forms import ClientQuestionForm

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