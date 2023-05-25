from django.core.management.base import BaseCommand
from posts.models import Tag
from faker import Faker


class Command(BaseCommand):
    help = 'Create random tags'

    def add_arguments(self, parser):
        parser.add_argument('num_tags', type=int)

    def handle(self, *args, **options):
        faker = Faker()
        num_tags = options['num_tags']
        for _ in range(num_tags):
            Tag.objects.create(
                name=faker.word()
            )

        self.stdout.write(self.style.SUCCESS(f'{num_tags} tags created with success!'))

