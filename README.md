# 🎶📖📑🕮 Haggadot 🕮📑📖🎶

## 👷🚧 🚧 🚧 WIP 🚧 🚧 🚧👷

## Prerequisites:

* Python 3.6
* pipenv

## Setup
* Clone repo
* `pipenv install`
* `python manage.py migrate`

## Load some books
```
python manage.py import_book PNX_MANUSCRIPTS000041407
python manage.py import_book PNX_MANUSCRIPTS000041667-2
```

## Load haggada text
```
python manage.py import_bookmarks
```

## Run server
* `python manage.py runserver`
* Enjoy: <http://localhost:8000/>

# Credits
* Haggada text from Sefaria/daat: <http://eph.sefaria.org/Pesach_Haggadah?lang=he>
