from csv import DictReader
from os.path import dirname, abspath

from django.core.management import BaseCommand

# Импорт моделей
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Команда для загрузки тестовых данных в БД из csv файлов"

    # Список переменных для импорта данных в модели
    models = (
        (
            (Ingredient, 'ingredients'),
        ),
    )

    root_dir = dirname(
        dirname(dirname(dirname(dirname(dirname(abspath(__file__)))))))

    def import_data(self):
        """ Метод импортирует пользователей, категории и жанры в БД. """

        for data in self.models:
            for model, file in data:
                with open(f'{self.root_dir}/data/{file}.csv',
                          encoding='utf-8') as f:
                    print(f'Начался импорт данных {file}')
                    for row in DictReader(f):
                        if not model.objects.filter(**row).exists():
                            model.objects.create(**row)
                print(f'Импорт данных {file} завершен.')

    def handle(self, *args, **options):
        """ Агрегирующий метод, который вызывается с помощью команды import
        и добавляет тестовые данные в БД. """

        self.import_data()
