from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User, Profile


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        for _ in range(total):
            User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password=fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
                role=fake.random_element(elements=('admin', 'editor', 'blogger'))
            )
        self.stdout.write(self.style.SUCCESS(f'{total} users created with success!'))

        for user in User.objects.all():
            Profile.objects.create(
                user=user,
                bio=fake.text(max_nb_chars=200),
                image=None  # Since faker can't generate an image, setting this to None
            )
        self.stdout.write(self.style.SUCCESS(f'{total} profiles created with success!'))
