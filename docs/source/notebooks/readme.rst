Prueba-Django-REST-Backend-Senior - Getting started
===================================================

Welcome to our Django REST API project! This API allows for managing
users, user profiles, blog posts, comments, likes and tags. Whether you
are an admin, editor, or blogger, you can use this API to meet your
requirements and manage all your content in a structured and efficient
manner.

Installation (from GitHub)
--------------------------

To get started, you need to clone the repository from GitHub to your
local machine. After cloning the repo, navigate to the main project
directory and install the required dependencies using pip. Here’s how
you do it:

.. code:: ipython3

    $ git clone https://github.com/YeisonCardona/Prueba-Django-REST-Backend-Senior.git
    $ cd Prueba-Django-REST-Backend-Senior
    $ pip install -r requirements.txt 

Setting up
----------

Before you can start using the application, you need to set up your
database. Django makes this easy with the ‘migrate’ command, which will
create the necessary database tables according to your models. After
setting up your database, you need to create a superuser account that
has all permissions to manage the API:

.. code:: ipython3

    $ cd blog
    $ python manage.py migrate
    $ python manage.py createsuperuser --username superuser --email super@mail.com

Generate test dataset
---------------------

You can populate your database with some test data. This is useful for
testing out the API’s functionality before deploying it to a live
environment. To generate the test data, run the ‘create_fake_data.sh’
script. The output will tell you how many users, profiles, tags, posts,
comments, and likes were created:

.. code:: ipython3

    $ . ./create_fake_data.sh

.. code:: ipython3

    16 users created with success!
    16 profiles created with success!
    32 tags created with success!
    64 posts created with success!
    256 comments created with success!
    1024 likes created with success!

Now, you’re all set! You can start exploring the API and testing its
features.

DRF - Web browsable API
-----------------------

http://localhost:8000/

This link leads to the Django Rest Framework (DRF) Web Browsable API for
our project. This interface allows for easy navigation, creation, and
manipulation of the API endpoints directly from the web browser. It’s
perfect for quick testing and debugging, providing a user-friendly
interface for interacting with our data models.

Note: Please ensure that the server is running locally on your machine
for this link to work. You can start the server using the following
command in the root directory of the project:
``python manage.py runserver``

DRF - Web browsable API
-----------------------

http://localhost:8000/swagger/

This link leads to the Swagger UI documentation of our API. Swagger is a
set of open-source tools built around the OpenAPI Specification that can
help you design, build, document, and use REST APIs. It makes it easy
for developers to understand and work with our API by providing an
interactive documentation with a sleek user interface.

The Swagger UI allows you to explore and interact with all the API
endpoints, observe the responses, and even try out different parameters
and body requests.

Note: Please ensure that the server is running locally on your machine
for this link to work. You can start the server using the following
command in the root directory of the project:
``python manage.py runserver``

