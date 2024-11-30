How to run the project? 
-Download the source code on your local machine. 
-Make sure you have python installed.
-Once you have python installed, move to the project directory on your command prompt and run 'pip install -r requirements.txt'
- Now, you need to make migration, using the following commands:
  python manage.py makemigrations
  python manage.py migrate
- Once the migrations are succesfully done, run the command:
  python manage.py runserver
  this will start your project on localhost on port 8000 : http://localhost:8000/

To connect to the backend visit the frontend respository: [https://github.com/Palveet/resume-builder](https://github.com/Palveet/resume_builder_react)
