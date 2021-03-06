# Getting Started with Wagtail and GraphQL
I was recently tasked with adding a CMS to an existing React application using `GraphQL` and `python+django` on the back end.  Wagtail was a perfect fit for this task because it is a simple drop in as a `django` app, and was easy to expose to our `GraphQL` layer.  

The ability to integrate `wagtail` with our existing domain models at the `GraphQL` layer meant that we could leverage our existing API calls _inside_ an article with little more than a `ForeignKey` and a small `resolver`.

## Assumptions
* Starting from blank repository
* python 3.6
* virtualenv

## Installing Wagtail
* Follow instructions here: http://docs.wagtail.io/en/v1.9/getting_started/
* Stop the server

## Add Blog App
Run `python manage.py startapp blog`

Update `blog/models.py` with the following content:

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
Run `pip install "graphene-django==1.2"`

## Configure Graphene
Add additional graphene settings to `base.py`

``` python
GRAPHENE = {
  'SCHEMA': 'api.schema.schema',
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
Add two new imports to your `urls.py` file.

``` python
  from django.views.decorators.csrf import csrf_exempt
  from graphene_django.views import GraphQLView
```

Add two new URLs to your `urls.py` file just above the wagtail entry.
``` python
  url(r'^api/graphql', csrf_exempt(GraphQLView.as_view())),
  url(r'^api/graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True, pretty=True))),
```

## Add new apps to settings
``` python
INSTALLED_APPS = (
    # ... previously installed apps
    'api',
    'blog',
    'graphene_django',
)
```

## Commit new models
Run `python manage.py makemigrations`

Run `python manage.py migrate`

## Start website
Run `python manage.py runserver`

## Make a new blog entry
* Access the wagtail admin at [http://localhost:8000/admin/]().
* Using the menu, navigate to `Explorer` > `Home Page` and click `Add Child Page`
* Choose to add a new page of type `BlogPage`
* Fill in all the fields
* Save & Publish

## Test graphql
Navigate to [http://localhost:8000/api/graphiql](http://localhost:8000/api/graphiql/?query=query%20articles%20%7B%0A%20%20articles%20%7B%0A%20%20%20%20id%0A%20%20%20%20title%0A%20%20%20%20date%0A%20%20%20%20intro%0A%20%20%20%20body%0A%20%20%7D%0A%7D&operationName=articles) and run the query below:

```javascript
query articles {
  articles {
    id
    title
    date
    intro
    body
  }
}
```
