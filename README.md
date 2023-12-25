# django_decision_tree

## Step 1:

Create a .env file with the following

```bash
# the address to your db.sqlite 3 file in the same directory as questions
DB_NAME=my_db

# base url of ur host server
BASE_URL=http://127.0.0.1:8000/
```

## Step 2

Create a virtual environment
and start your virtual environment

```bash
py -m venv .venv

source .venv/Scripts/activate
```

## Step 3

install required files using

```bash
pip install -r req.txt
```

## Step 4

Run server with the following.

```bash
py manage.py runserver
```
