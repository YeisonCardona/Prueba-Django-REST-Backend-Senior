```python

```

# Prueba-Django-REST-Backend-Senior - Getting started

Welcome to our Django REST API project! This API allows for managing users, user profiles, blog posts, comments, likes and tags. Whether you are an admin, editor, or blogger, you can use this API to meet your requirements and manage all your content in a structured and efficient manner.

## Installation (from GitHub)

To get started, you need to clone the repository from GitHub to your local machine. After cloning the repo, navigate to the main project directory and install the required dependencies using pip. Here's how you do it:


```python
$ git clone https://github.com/YeisonCardona/Prueba-Django-REST-Backend-Senior.git
$ cd Prueba-Django-REST-Backend-Senior
$ pip install -r requirements.txt 
```

## Setting up

Before you can start using the application, you need to set up your database. Django makes this easy with the 'migrate' command, which will create the necessary database tables according to your models. After setting up your database, you need to create a superuser account that has all permissions to manage the API:


```python
$ cd blog
$ python manage.py migrate
$ python manage.py createsuperuser --username superuser --email super@mail.com
```

## Generate test dataset

You can populate your database with some test data. This is useful for testing out the API's functionality before deploying it to a live environment. To generate the test data, run the 'create_fake_data.sh' script. The output will tell you how many users, profiles, tags, posts, comments, and likes were created:


```python
$ . ./create_fake_data.sh
```


```python
16 users created with success!
16 profiles created with success!
32 tags created with success!
64 posts created with success!
256 comments created with success!
1024 likes created with success!
```

Now, you're all set! You can start exploring the API and testing its features.

## DRF - Web browsable API 
[http://localhost:8000/](http://localhost:8000/)

This link leads to the Django Rest Framework (DRF) Web Browsable API for our project. This interface allows for easy navigation, creation, and manipulation of the API endpoints directly from the web browser. It's perfect for quick testing and debugging, providing a user-friendly interface for interacting with our data models. 

Note: Please ensure that the server is running locally on your machine for this link to work. You can start the server using the following command in the root directory of the project: `python manage.py runserver`

## Swagger UI documentation
[http://localhost:8000/swagger/](http://localhost:8000/swagger/)


This link leads to the Swagger UI documentation of our API. Swagger is a set of open-source tools built around the OpenAPI Specification that can help you design, build, document, and use REST APIs. It makes it easy for developers to understand and work with our API by providing an interactive documentation with a sleek user interface. 

Note: Please ensure that the server is running locally on your machine for this link to work. You can start the server using the following command in the root directory of the project: `python manage.py runserver`

## Read the Docs
[https://prueba-django-rest-backend-senior.readthedocs.io/en/latest/](https://prueba-django-rest-backend-senior.readthedocs.io/en/latest/)


This link will take you to our project's documentation hosted on Read the Docs. Here you'll find detailed information about the project's structure, functionality, and how to use it. The documentation is carefully written to guide you through the setup process, demonstrate the usage of the project, and provide insights into the codebase.

## GitHub

[https://github.com/YeisonCardona/Prueba-Django-REST-Backend-Senior](https://github.com/YeisonCardona/Prueba-Django-REST-Backend-Senior)

The link above directs you to our project's GitHub repository. Here, you can access the complete codebase, check the latest commits, download the source code, or clone the repository for your own use. The repository provides a comprehensive view of the project's development history and its current state.
