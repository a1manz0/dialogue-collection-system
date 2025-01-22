# Generated by Django 5.1.5 on 2025-01-22 22:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dialogue_example', models.TextField(default='', help_text='Введите пример диалога в формате:\nКлиент: [сообщение]\nМенеджер: [ответ]\n...', verbose_name='Пример диалога')),
                ('topic', models.CharField(choices=[('course_info', 'Информация о курсах'), ('pricing', 'Стоимость обучения'), ('schedule', 'Расписание занятий'), ('trial', 'Пробное занятие'), ('age', 'Возрастные группы'), ('technical', 'Технические вопросы'), ('other', 'Другое')], max_length=20, verbose_name='Тема диалога')),
                ('complexity', models.CharField(choices=[('simple', 'Простой вопрос'), ('crm', 'Требуется проверка в CRM'), ('complex', 'Сложный вопрос')], max_length=20, verbose_name='Сложность ответа')),
                ('requires_crm', models.BooleanField(default=False, verbose_name='Требуется проверка в CRM')),
                ('tags', models.CharField(blank=True, help_text='Разделяйте теги запятыми', max_length=200, verbose_name='Теги')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_questions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Вопрос клиента',
                'verbose_name_plural': 'Вопросы клиентов',
                'ordering': ['-created_at'],
            },
        ),
    ]
