from django import template
from news.models import Category

register = template.Library()

@register.inclusion_tag('news/categories_tpl.html')
def show_categories():
	categories = Category.objects.all()
	return {"categories": categories}