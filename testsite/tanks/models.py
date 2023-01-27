from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from PIL import Image


class Tank(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    # blank=True - поле может быть пустым
    slug = models.SlugField(max_length=250, unique=True,
                            db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name='Фото ')
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    cat = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):  # для красивого вывода в консоле
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-time_create']


class Category(models.Model):
    # поиск по индексу т.е быстрее
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=250, unique=True,
                            db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['id']



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='images/avatar.png', upload_to='images')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Comment(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    tank = models.ForeignKey(
        Tank, verbose_name="Танк", on_delete=models.CASCADE)
    
    profile = models.ForeignKey(
        Profile, verbose_name="Профиль", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.email} - {self.tank}"

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

