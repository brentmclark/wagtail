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

update `models.py` to the code below:

``` python
# Taken From http://docs.wagtail.io/en/v1.8.1/getting_started/tutorial.html

from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]
```

## Installing Graphene
`pip install "graphene-django==1.2"`

## Configure Graphene
Add graphene_django to installed apps in `base.py`:

``` python
INSTALLED_APPS = (
    # ...
    'graphene_django',
)
```

Add additional graphene settings to `base.py`

``` python
GRAPHIQL_GRAPHQL_URL = '/api/graphql'
}
```

## Add API App
Make a new folder at the root of `mysite` called `api`

### Add apps.py
Make a new file inside the new `api` folder called `apps.py`, and paste in the following:

``` python
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
```

### Add schema.py
Make another new file inside the `api` folder named `schema.py` with the following contents:

``` python
from __future__ import unicode_literals
import graphene
from graphene_django import DjangoObjectType
from blog.models import BlogPage

from django.db import models

class ArticleNode(DjangoObjectType):
    class Meta:
        model = BlogPage
        only_fields = ['id', 'title', 'date', 'intro', 'body']


class Query(graphene.ObjectType):
    articles = graphene.List(ArticleNode)

    @graphene.resolve_only_args
    def resolve_articles(self):
        return BlogPage.objects.live()

schema = graphene.Schema(query=Query)
```

## Configure URLS
Add the two URLs below to your `urls.py` file just above the wagtail entry
``` python
  url(r'^graphql', csrf_exempt(GraphQLView.as_view())),
  url(r'^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True, pretty=True))),
```

## Add all new apps to settings
``` python
INSTALLED_APPS = (
    # ... previously installed apps
    'api',
    'blog',
    'graphene_django',
)
```
