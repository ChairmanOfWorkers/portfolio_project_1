from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Tag, Post
from django.db.models import F


class Home(ListView):
	#Показывает статьи на главной странице
	model = Post
	template_name = 'news/home_page.html'
	context_object_name = 'posts'
	paginate_by = 6
	ordering = ['-views']

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Classic News Design'
		return context

class PostsByCategory(ListView):
	#Показывает посты одной категории
	template_name = 'news/home_page.html'
	context_object_name = 'posts'
	paginate_by = 6
	allow_empty = False

	def get_queryset(self):
		return Post.objects.filter(category__slug=self.kwargs['slug'])

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = Category.objects.get(slug=self.kwargs['slug'])
		return context

class PostsByTag(ListView):
	#Показывает посты с одинаковым тегом
	template_name = 'news/home_page.html'
	context_object_name = 'posts'
	paginate_by = 6
	allow_empty = False

	def get_queryset(self):
		return Post.objects.filter(tags__slug=self.kwargs['slug'])

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
		return context

class GetPost(DetailView):
	#Показывает один пост на новой странице
	model = Post
	template_name = 'news/single_page.html'
	context_object_name = 'posts'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		self.object.views = F('views') + 1
		self.object.save()
		self.object.refresh_from_db()
		return context

class Search(ListView):
	#Поиск постов на сайте(при вводе кирилицей регистр учитывается, при использовании латиницы нет)
	template_name = 'news/search.html'
	context_object_name = 'posts'
	paginate_by = 6

	def get_queryset(self):
		return Post.objects.filter(title__icontains=self.request.GET.get('s'))

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['s'] = f"s={self.request.GET.get('s')}&"
		return context