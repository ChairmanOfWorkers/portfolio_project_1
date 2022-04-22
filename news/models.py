from django.db import models
from django.urls import reverse


class Category(models.Model):
	#Модель категории: Включает только название категории и слаг ссылку на нее
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('category', kwargs={"slug": self.slug})

	class Meta:
		ordering = ['title']
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

class Tag(models.Model):
	#Модель тега: Включает только название тега и слаг ссылку на него
	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, verbose_name='url', unique=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('tag', kwargs={"slug": self.slug})

	class Meta:
		ordering = ['title']
		verbose_name = 'Тег'
		verbose_name_plural = 'Теги'	

class Post(models.Model):
	#Модель поста. Подключен к категории(один к одному) и тегу(один ко многим)
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опублековано')
	photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=False)
	views = models.IntegerField(default=0, verbose_name='Количество просмотров')
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
	tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post', kwargs={"slug": self.slug})

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'