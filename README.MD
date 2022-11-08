# COMPLETE CBT APPLICATION BASE ON DJANGO

## Technologies

- Django 4
- CSS by bootstrap 5
- Rich editor by summernote
- Icons from fontawesome
- Jquery and Jquery countdown.

## Features

- Timezones aware
- Unlimited Exams with unlimited questions
- Rich editor to add any kind of content
- Pick question to exam from the quesiton bank
- Auto timeout and auto submit.
- View students score
- Configurable number of choices per exam
- Make everything configurable\*

## Installation

It's best to install Python projects in a Virtual Environment use <a href="https://docs.python.org/3/library/venv.html">venv</a> or virtualenvwrapper.
Once you have set up a VE, clone this project

```bash
git clone https://github.com/adigunsherif/cbt.git
```

Then

```bash
cd cbt
```

Run

```python
pip install -r requirements.txt #install required packages
copy example.env.txt and rename to .env Then, set the the appropriate values
python manage.py migrate # run first migration
python manage.py runserver # run the server
```

Then locate http://172.0.0.1:8000
