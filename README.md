# Apartment Review Api
An Apartment review api to help people rate, share and express their thoughts and experiences on previously occupied apartments.

# Technology
 <img src='https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue'> <img src='https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green'>
<img src='https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white'>

# Database ERD
https://drawsql.app/teams/gabriels-team-1/diagrams/apartment-review-api

# Documentation 

# Setup
To set up this project on your local machine,<br>

1. Fork the repo and clone it to your local machine<br>

2. In your terminal, navigate to the project root folder <code>Apartment_Review_Api</code> create a virtual environment <code>python3 -m venv env</code> , then activate it <code>source env/bin/activate</code> (<i>for linux/unix</i>) or <code>env/scripts/activate</code> (<i>for windows</i>)<br>

3. Install the project dependencies <code>pip install -r requirements.txt </code> <br>

4. Make your migrations <code>python manage.py migrate</code> or run makemigrations again if necessary <code>python manage.py makemigrations</code> <br>

5. Start the django development server <code>python manage.py runserver</code> or use the gunicorn server <code>gunicorn review_project.wsgi</code> <br>

6. Make your api calls

<br><br>
<strong>NOTE</strong><br>
* Remember to generate a generate or set a new secret key in the <code>settings.py</code> file. you can quickly generate one in the terminal by running <code>python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'</code>
