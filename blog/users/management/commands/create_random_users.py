from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User, Profile
import csv
import os


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        created_users = []

        credentials = []
        for _ in range(total):
            credentials.append([fake.unique.user_name(),
                                fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
                                fake.random_element(elements=('admin', 'editor', 'blogger'))
                                ])
            created_users.append(User.objects.create_user(
                username=credentials[-1][0],
                email=fake.unique.email(),
                password=credentials[-1][1],
                role=credentials[-1][2],
            ))
        self.stdout.write(self.style.SUCCESS(f'{total} users created with success!'))

        for user in created_users:
            Profile.objects.create(
                user=user,
                bio=fake.text(max_nb_chars=200),
                image=None  # Since faker can't generate an image, setting this to None
            )

        self.stdout.write(self.style.SUCCESS(f'{total} profiles created with success!'))

        with open(os.path.join('faker', 'users.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password', 'role'])
            for row in credentials:
                writer.writerow(row)


