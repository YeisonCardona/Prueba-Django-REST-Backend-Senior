from django.core.management.base import BaseCommand
from posts.models import Like, Post, Comment
from users.models import User
import random


class Command(BaseCommand):
    help = 'Create random likes'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of likes to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for _ in range(total):
            is_like_for_post = random.choice([True, False])
            if is_like_for_post:
                Like.objects.create(
                    user=User.objects.order_by('?').first(),
                    post=Post.objects.order_by('?').first(),
                    comment=None,
                )
            else:
                Like.objects.create(
                    user=User.objects.order_by('?').first(),
                    post=None,
                    comment=Comment.objects.order_by('?').first(),
                )
        self.stdout.write(self.style.SUCCESS(f'{total} likes created with success!'))
