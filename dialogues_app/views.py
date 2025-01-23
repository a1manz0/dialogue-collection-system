from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Dialogue, Message
from .forms import DialogueWithMessagesForm
import json
import csv

class DialogueListView(LoginRequiredMixin, ListView):
    model = Dialogue
    template_name = 'dialogues_app/dialogue_list.html'
    context_object_name = 'dialogues'
    paginate_by = 10

    def get_queryset(self):
        return (Dialogue.objects.select_related('created_by')
                .prefetch_related('messages')
                .order_by('-created_at'))

class DialogueCreateView(LoginRequiredMixin, CreateView):
    model = Dialogue
    form_class = DialogueWithMessagesForm
    template_name = 'dialogues_app/dialogue_form.html'
    success_url = reverse_lazy('dialogue_list')

    def form_valid(self, form):
        # Сохраняем диалог
        form.instance.created_by = self.request.user
        dialogue = form.save()

        # Получаем сообщения из формы
        messages_data = self.request.POST.get('messages')
        if messages_data:
            try:
                messages = json.loads(messages_data)
                # Создаем сообщения
                for msg in messages:
                    Message.objects.create(
                        dialogue=dialogue,
                        author=msg['author'],
                        text=msg['text']
                    )
            except json.JSONDecodeError:
                pass  # Игнорируем ошибки парсинга JSON

        return redirect(self.success_url)

class DialogueUpdateView(LoginRequiredMixin, UpdateView):
    model = Dialogue
    form_class = DialogueWithMessagesForm
    template_name = 'dialogues_app/dialogue_form.html'
    success_url = reverse_lazy('dialogue_list')

    def form_valid(self, form):
        dialogue = form.save()
        
        # Удаляем старые сообщения
        dialogue.messages.all().delete()
        
        # Получаем новые сообщения из формы
        messages_data = self.request.POST.get('messages')
        if messages_data:
            try:
                messages = json.loads(messages_data)
                # Создаем новые сообщения
                for msg in messages:
                    Message.objects.create(
                        dialogue=dialogue,
                        author=msg['author'],
                        text=msg['text']
                    )
            except json.JSONDecodeError:
                pass

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = []
        for message in self.object.messages.all().order_by('created_at'):
            messages.append({
                "author": message.author,
                "text": message.text
            })
        context['initial_messages'] = json.dumps(messages, ensure_ascii=False)
        return context

class DialogueDeleteView(LoginRequiredMixin, DeleteView):
    model = Dialogue
    template_name = 'dialogues_app/dialogue_confirm_delete.html'
    success_url = reverse_lazy('dialogue_list')

@login_required
def export_json(request):
    dialogues = Dialogue.objects.prefetch_related('messages').all()
    data = []
    
    for dialogue in dialogues:
        messages_data = []
        for message in dialogue.messages.all():
            messages_data.append({
                'author': message.get_author_display(),
                'text': message.text,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        data.append({
            'id': dialogue.id,
            'topic': dialogue.get_topic_display(),
            'requires_crm': dialogue.requires_crm,
            'messages': messages_data,
            'created_by': dialogue.created_by.username,
            'created_at': dialogue.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    response = HttpResponse(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="dialogues.json"'
    return response

@login_required
def export_csv(request):
    dialogues = Dialogue.objects.prefetch_related('messages').all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dialogues.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID диалога', 'Тема', 'Требуется CRM', 'Автор', 'Текст', 'Создал', 'Дата создания'])
    
    for dialogue in dialogues:
        for message in dialogue.messages.all():
            writer.writerow([
                dialogue.id,
                dialogue.get_topic_display(),
                'Да' if dialogue.requires_crm else 'Нет',
                message.get_author_display(),
                message.text,
                dialogue.created_by.username,
                message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
    
    return response