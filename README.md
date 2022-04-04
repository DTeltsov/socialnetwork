# socialnetwork

This is API for mini social network.<br>
I used Django REST Framework as base(i will call it DRF for simplicity). <br>
I used [Simple_jwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for jwt authorization, because it was in DRF dosc for jwt.<br>
And also i used PostgreSQL as db.

## Installing

### Dependencies

Run in your terminal next commands <br>
<code>git clone https://github.com/DTeltsov/socialnetwork.git</code><br>
<code>cd ./path/to/socialnetwork</code><br>
<code>pip install -r /path/to/requirements.txt</code>

### Database

In settings.py change all data to yours.<br>
<code>
  DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'networkdb',

        'USER': 'user',

        'PASSWORD': 'password',

        'HOST': 'localhost',

        'PORT': '',

    }
}</code><br>
Then run <br>
<code>python manage.py makemigrations</code><br>
<code>python manage.py migrate</code>

### Run

<code>python manage.py runserver</code>

## Usage

#### Sing up

Send **POST** request to */api/v1/user/* with body <code>{'username':'your username', 'password':'your password'}</code>. <br>
Optionaly you can add <code>first_name, last_name</code> fields.

#### Login

Send **POST** request to */api/v1/token/* with body <code>{'username':'your username', 'password':'your password'}</code>. <br>
You will get your acsess and refresh jwt tokens.

#### User

- You can acsess to users list via sending **GET** request to */api/v1/user/* <br>

- You can get specific user via sending **GET** request to */api/v1/user/users id/* <br>

- You can delete your account via sending **DELETE** request to */api/v1/user/your user id/* <br>

  - (you will get rejected if you try to delete another user) <br>

- You can patch or put your account data via **PATCH** or **PUT** request to */api/v1/user/your user id/* <br>

  - (you will get rejected if you try to update another user) <br>

-You can get user activity info via sending **GET** request to */api/v1/activity/*

#### Post

- You can acsess to posts list via sending **GET** request to */api/v1/post/* <br>

- You can get specific post via sending **GET** request to */api/v1/post/post id/* <br>

- You can post your post via sending **POST** request to */api/v1/post/* with body <code>{'text':'your text'}</code>

- You can delete your post via sending **DELETE** request to */api/v1/post/your post id/* <br>

  - (you will get rejected if you try to delete another users post) <br>

- You can patch or put your post via **PATCH** or **PUT** request to */api/v1/post/your post id/* <br>

  - (you will get rejected if you try to update another users post) <br>

- You can like/dislike post via sending **POST** request to */api/v1/post/post id/rate/* with body <code>{'liked':True/False}</code> <br>

- You can check statistics of your post for specific time period via sending **GET** request to */api/v1/post/your post id/analitics/&date_to=&date_from=* <br>
