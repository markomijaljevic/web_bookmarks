# Web Bookmarks API

## API routes
- Project Contains basic CRUD API actions.
  - Create (POST /api/bookmark/)
  - Read (GET /api/bookmark/2/)
  - Update (PUT /api/bookmark/2/)
  - Delete (DELETE /api/bookmark/2/)

API is built using latest Django Web Framework and [Django REST framework](https://www.django-rest-framework.org/). 

# Requirements and Local Installation  
First, it is necessary to create a virtual environment. Either IDE will create it or it can be set manually.
To create manually a virtual environment we ran commands:

```
python -m venv venv
```
After creating a virtual environment it is necessary to activate it:  

On Windows:
```
venv\Scripts\activate
```
On Linux:
```
source venv\bin\activate
```

All the requirements necessary for the project to run are located in the requirements.txt file.  
To install requirements run:  
```
pip install -r requirements.txt 
```
Now initial migrations should be ran:
```
python manage.py makemigrations
python manage.py migrate
```

After successfully activating the environment and installing all the 
requirements all we have to do now is to run the Django server and create the SuperUser:
*(SuperUser is for testing Authenticated vs Anonymous user)*.

```
python manage.py createsuperuser
python manage.py runserver
```

Once the server is running each API endpoint can be tested by visiting its own routes:
- **/get/** (list all private and public) **if anonymous user list only public**
- **/retrieve/id/** (retrieve specific bookmark)
- **/create/** (add bookmark)
- **/update/id/** (update specific bookmark)
- **/delete/id/** (delete specific bookmark)


# Running Tests

The bookmark application has provided test cases for different scenarios.
To be sure that everything is as expected tests should be run.

Run test:
```
python manage.py test
```

All test should pass for everything to work.