from django.test import TestCase
from django.urls import reverse
from django.template import Context, Template

from .models import Menu, MenuItem


class MenuModelTest(TestCase):
    """Тесты для модели Menu."""
    def setUp(self):
        """Создает экземпляр меню перед каждым тестом."""
        self.menu = Menu.objects.create(name='Main Menu')

    def test_menu_str(self):
        """Проверяет строковое представление модели Menu."""
        self.assertEqual(str(self.menu), 'Main Menu')


class MenuItemModelTest(TestCase):
    """Тесты для модели MenuItem."""
    def setUp(self):
        """Создает экземпляр меню и пункта меню перед каждым тестом."""
        self.menu = Menu.objects.create(name='Main Menu')
        self.menu_item = (
            MenuItem.objects.create(menu=self.menu, name='Home', url='/home/'))

    def test_menu_item_str(self):
        """Проверяет строковое представление модели MenuItem."""
        self.assertEqual(str(self.menu_item), 'Home')

    def test_get_absolute_url(self):
        """Проверяет метод get_absolute_url для URL."""
        self.menu_item.url = '/home/'
        self.assertEqual(self.menu_item.get_absolute_url(), '/home/')

    def test_get_absolute_url_named(self):
        """Проверяет метод get_absolute_url для named_url."""
        self.menu_item.named_url = 'home'
        self.assertNotEqual(self.menu_item.get_absolute_url(), '/home/')


class MenuViewTest(TestCase):
    """Тесты для представлений меню."""
    def setUp(self):
        """Создает экземпляр меню и пункта меню перед каждым тестом."""
        self.menu = Menu.objects.create(name='Main Menu')
        self.menu_item = (
            MenuItem.objects.create(menu=self.menu, name='Home', url='/home/'))

    def test_index_view(self):
        """
        Проверяет, что представление индекса возвращает
        статус 200 и использует правильный шаблон.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/index.html')


class MenuTemplateTest(TestCase):
    """Тесты для рендеринга шаблона меню."""
    def test_menu_template_rendering(self):
        """Проверяет, что меню корректно рендерится в шаблоне."""
        menu = Menu.objects.create(name='Main Menu')
        MenuItem.objects.create(menu=menu, name='Home', url='/home/')
        template = Template('{% load menu_tags %}{% draw_menu "Main Menu" %}')
        rendered = (
            template.render(Context({'request': self.factory.get('/home/')})))
        self.assertIn('<li class="active">', rendered)
        self.assertIn('Home', rendered)
