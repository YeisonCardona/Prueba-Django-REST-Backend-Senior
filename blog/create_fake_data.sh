#!/usr/bin/bash

mkdir -p faker
python manage.py create_random_users 16
python manage.py create_random_tags 32
python manage.py create_random_posts 64
python manage.py create_random_comments 256
python manage.py create_random_likes 1024
