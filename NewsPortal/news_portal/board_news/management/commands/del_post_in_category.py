from django.core.management.base import BaseCommand
from board_news.models import Post, Category


class Command(BaseCommand):
    help = 'Удалить посты в выбранной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.write(
            f'Хотите удалить посты в категории "{options["category"]}"? Да/Нет')
        answer = input()

        if answer != 'Да':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(categories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Посты в категории "{options["category"]}" удалены!'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR('Такая категория не найдена'))
