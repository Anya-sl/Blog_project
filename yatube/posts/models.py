from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    """Класс, представляющий модель сообщества."""

    title = models.CharField(max_length=200, verbose_name='Имя сообщества')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Класс, представляющий модель поста."""

    text = models.TextField(verbose_name='Содержание поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              blank=True, null=True,
                              related_name='posts',
                              verbose_name='Сообщество',)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.text[:15]
