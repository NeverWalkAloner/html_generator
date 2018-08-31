[![Build Status](https://travis-ci.org/NeverWalkAloner/html_generator.svg?branch=master)](https://travis-ci.org/NeverWalkAloner/html_generator)

### Install

```
pip install -r requirements.txt
```

### Quickstart

1. Create markdown file inside *content* directory.

2. Add to the file something like this:

```
Title: My First Article
Date: 2018-08-31 10:20
Category: Blog

Some interesting content **here**.

```

3. run manage.py to generate html file in *output* directory:

```
python manage.py --sitename "My static page"
```

### Features

#### Categories

You can create as many categories as you want.

#### Pagination

To enable pagination within whole project use *paginatedby* argument:

```
python manage.py --sitename "My static page" --paginatedby 2
```
