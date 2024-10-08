from django import template
from django.utils.safestring import mark_safe
from django.urls import resolve

from menu.models import Menu

register = template.Library()


def build_menu_tree(items, current_url):
    """Создает древовидную структуру меню."""
    tree = {}
    for item in items:
        tree[item.id] = {
            'item': item,
            'children': [],
            'is_active': item.get_absolute_url() == current_url
        }
    for item in items:
        if item.parent:
            tree[item.parent_id]['children'].append(tree[item.id])
    return [v for k, v in tree.items() if v['item'].parent is None]


def render_menu_tree(tree):
    """Рендерит HTML-структуру для древовидного меню."""
    html = '<ul>'
    for node in tree:
        item = node['item']
        classes = 'active' if node['is_active'] else ''
        html += f'<li class="{classes}">' \
                f'<a href="{item.get_absolute_url()}">{item.name}</a>'
        if node['children']:
            html += render_menu_tree(node['children'])
        html += '</li>'
    html += '</ul>'
    return html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    """Тег шаблона для отрисовки древовидного меню."""
    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
        current_url = resolve(context['request'].path_info).url_name
        items = menu.items.all()
        tree = build_menu_tree(items, current_url)
        return mark_safe(render_menu_tree(tree))
    except Menu.DoesNotExist:
        return ''
