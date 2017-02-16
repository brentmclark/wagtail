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