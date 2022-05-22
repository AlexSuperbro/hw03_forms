from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True
    )
    description = models.TextField(
        'Описание'
    )

    class Meta:
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return (self.title)[:settings.CONST_THIRTY]


class Post(models.Model):
    text = models.TextField(
        'Текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.text[:settings.CONST_THIRTY]
