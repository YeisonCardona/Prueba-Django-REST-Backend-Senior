import random
from django.core.management.base import BaseCommand
from posts.models import Post, Tag
from users.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'Create random posts'

    def add_arguments(self, parser):
        parser.add_argument('num_posts', type=int)

    def handle(self, *args, **options):
        faker = Faker()
        num_posts = options['num_posts']
        tags = list(Tag.objects.all())
        for _ in range(num_posts):
            post = Post.objects.create(
                title=faker.sentence(),
                content=faker.text(),
                author=random.choice(User.objects.all()),
                category=faker.word(),
            )
            post.tags.add(*random.sample(tags, k=random.randint(0, 5)))

        self.stdout.write(self.style.SUCCESS(f'{num_posts} posts created with success!'))
