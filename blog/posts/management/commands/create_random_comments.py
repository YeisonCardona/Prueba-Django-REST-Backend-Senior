from django.core.management.base import BaseCommand
from posts.models import Comment, Post
from users.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'Create random comments'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of comments to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        for _ in range(total):
            Comment.objects.create(
                user=User.objects.order_by('?').first(),
                post=Post.objects.order_by('?').first(),
                text=fake.text(),
            )
        self.stdout.write(self.style.SUCCESS(f'{total} comments created with success!'))
