# wagtail
Wagtail CMS for python+django

## Opening Paragraph
stuff and/or things go here

## Assumptions
* Starting from blank repository
* python 3.6
* virtualenv
* all that jazz

## New Repository

## Create Virtual Environment
`virtualenv -p /usr/local/bin/python3.6 venv`

## Activate Virtual Environment

`source venv/bin/activate`

## Installing Wagtail
Follow instructions here: http://docs.wagtail.io/en/v1.9/getting_started/
kill the server

## Add Blog App
`python manage.py startapp blog`
Add the blog app to INSTALLED APPS

``` python
INSTALLED_APPS = (     
  #... previously installed apps     
  ‘blog', 
)
```

## Installing Graphene
`pip install "graphene-django==1.2"`

## Configure Graphene
Add graphene_django to installed apps:

``` python
INSTALLED_APPS = (
    # ...
    'graphene_django',
)
```

## Create Schema
## Configure URLS
## Add API app to settings
