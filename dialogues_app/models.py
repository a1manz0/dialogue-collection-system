from django.db import models
from django.contrib.auth.models import User


class Dialogue(models.Model):
    TOPIC_CHOICES = [
        ('course_info', 'Информация о курсах'),
        ('pricing', 'Стоимость обучения'),
        ('schedule', 'Расписание занятий'),
        ('trial', 'Пробное занятие'),
        ('age', 'Возрастные группы'),
        ('technical', 'Технические вопросы'),
        ('other', 'Другое'),
    ]

    topic = models.CharField('Тема', max_length=50, choices=TOPIC_CHOICES)
    requires_crm = models.BooleanField('Требуется доступ к CRM', default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создал')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'
        ordering = ['-created_at']

    def __str__(self):
        return f'Диалог {self.id} - {self.get_topic_display()}'


class Message(models.Model):
    AUTHOR_CHOICES = [
        ('user', 'Клиент'),
        ('assistant', 'Менеджер'),
    ]

    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, related_name='messages')
    author = models.CharField('Автор', max_length=20, choices=AUTHOR_CHOICES)
    text = models.TextField('Текст сообщения')
    created_at = models.DateTimeField('Время создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.get_author_display()}: {self.text[:50]}...' 