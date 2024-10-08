from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    """
    Вспомогательный класс для отображения и редактирования элементов меню
    (MenuItem) в админке Django в табличном виде внутри формы редактирования
    меню (Menu).
    """
    model = MenuItem
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели Menu в админке Django."""
    inlines = [MenuItemInline]
