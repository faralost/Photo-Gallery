from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Photo(models.Model):
    image = models.ImageField(upload_to='images', verbose_name='Фото')
    caption = models.CharField(max_length=100, verbose_name='Подпись')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', verbose_name='Автор')
    album = models.ForeignKey('webapp.Album', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Альбом', related_name='photos')
    favorites = models.ManyToManyField(User, related_name='favorited_photos', blank=True)
    is_private = models.BooleanField(default=False, verbose_name='Приватный ли')

    def __str__(self):
        return f'{self.caption}'

    def get_absolute_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.pk})


class Album(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_private = models.BooleanField(default=False, verbose_name='Приватный ли')

    def __str__(self):
        return f'{self.name}'
