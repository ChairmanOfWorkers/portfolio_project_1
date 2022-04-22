from django import template
from news.models import Post, Tag

register = template.Library()

@register.inclusion_tag('news/popular_posts_tpl.html')
#Возвращает популярные посты
def get_popular(cnt=3):
	posts = Post.objects.order_by('-views')[:cnt]
	return {"posts": posts}

@register.inclusion_tag('news/tags_tpl.html')
#Возвращает теги
def get_tags():
	tags = Tag.objects.all()
	return {"tags": tags}