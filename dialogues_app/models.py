from django.db import models
from django.contrib.auth.models import User


class ClientQuestion(models.Model):
    TOPIC_CHOICES = [
        ('course_info', 'Информация о курсах'),
        ('pricing', 'Стоимость обучения'),
        ('schedule', 'Расписание занятий'),
        ('trial', 'Пробное занятие'),
        ('age', 'Возрастные группы'),
        ('technical', 'Технические вопросы'),
        ('other', 'Другое'),
    ]

    COMPLEXITY_CHOICES = [
        ('simple', 'Простой вопрос'),
        ('crm', 'Требуется проверка в CRM'),
        ('complex', 'Сложный вопрос'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dialogue_example = models.TextField(
        verbose_name="Пример диалога",
        help_text="Введите пример диалога в формате:\nКлиент: [сообщение]\nМенеджер: [ответ]\n...",
        default=""
    )
    topic = models.CharField(
        max_length=20,
        choices=TOPIC_CHOICES,
        verbose_name="Тема диалога"
    )
    complexity = models.CharField(
        max_length=20,
        choices=COMPLEXITY_CHOICES,
        verbose_name="Сложность ответа"
    )
    requires_crm = models.BooleanField(
        default=False,
        verbose_name="Требуется проверка в CRM"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_questions'
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Теги",
        help_text="Разделяйте теги запятыми"
    )
    
    class Meta:
        verbose_name = "Вопрос клиента"
        verbose_name_plural = "Вопросы клиентов"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_topic_display()} - {self.question[:50]}..." 