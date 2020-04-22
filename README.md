
# Analyzr

## Project setup 

#### Backend
##### Prerequisites (Optional, but rather useful):
   - create a python virtual environment **(python 3.7 !)**
   - do all backend project operations from inside the said venv

##### Project setup:
 0. Move into the backend directory: `cd backend` 
 1. Install the required python packages:  
 `pip install -r requirements.txt`
 4. **Important:** Before running any other command, copy the `.env.example` file  
 into a new file named `.env` (this is where django takes some important configuration  
 from, the server will not run without this)
 2. Make the migrations for the django apps (scs_auth, api_* and crawler):  
    `python manage.py makemigrations`  
    `python manage.py makemigrations api_auth`  
    `python manage.py makemigrations data_parsing` 
 
 3. Migrate:  
 `python manage.py migrate`  
 4. (Optional) Create admin user:  
 `python manage.py createsuperuser` and follow the prompted steps
 
##### Project run:
- Run the development server:  
`py manage.py runserver`
- (Optional) Check the admin page at  
<http://localhost:8000/admin>

#### Frontend (this is from an old project, ignore right now)
The frontend react app is located in the folder `/frontend`.  
Run all the fronted operations from inside that folder: `cd /frontend`
##### Prerequisites:
 - node 12.x.y (10 might work too)
 - npm 6.9.x
 
##### Project setup:
 1. Install the required node modules:  
 `npm install`
 
##### Project run:
- Run the local react development server:  
`npm start`
