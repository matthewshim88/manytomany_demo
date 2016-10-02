from __future__ import unicode_literals

from django.db import models

from ..new_login.models import User
# Create your models here.

class QuoteManager(models.Manager):
    def add_quote(self, data, id):
        errors = []
        user = User.objects.get(id=id)
        if not data['quote']:
            errors.append('Quote cannot be blank')
        if not data['quoted_by']:
            errors.append('Quote must have an author')
        else:
            existing_quote = self.filter(quote=data['quote'], added_by=user)
            if existing_quote:
                errors.append('That quote already exists')
        response = {}
        if errors:
            response['errors'] = errors
            response['created'] = False
        else:
            quote = Quotes.objects.create(quoted_by = data['quoted_by'], quote = data['quote'], added_by=user)
            new_quote = Quotes.objects.get(id=quote.id)
            # new_quote.fav_quotes.add(id)
            new_quote.save()
            response['created'] = True
            response['quote'] = quote
        return response

    def add_favorite(self, quote, id):
        response = {}
        find_quote = Quotes.objects.get(id=quote.id)
        find_quote.fav_quotes.add(id)
        find_quote.save()
        response['added'] = True
        response['quote'] = find_quote
        return response

    def remove_favorite(self, quote, id):
        response = {}
        find_quote = Quotes.objects.get(id=quote.id)
        find_quote.fav_quotes.remove(id)
        find_quote.save()
        response['removed'] = True
        return response


class Quotes(models.Model):
    quoted_by = models.CharField(max_length=200)
    quote = models.CharField(max_length=255)
    fav_quotes = models.ManyToManyField(User, related_name="fav_quotes")
    added_by = models.ForeignKey(User, related_name='added_by')
    date_added = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=QuoteManager()
